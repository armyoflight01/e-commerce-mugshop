from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from decimal import Decimal
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review


def get_cart(request):
    """Retrieves or creates the Cart instance for current user or session."""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # Migrate anonymous cart if it exists
        anon_cart = Cart.objects.filter(session_key=session_key).exclude(id=cart.id).first()
        if anon_cart:
            for item in anon_cart.items.all():
                existing = cart.items.filter(product=item.product, custom_engraving=item.custom_engraving).first()
                if existing:
                    existing.quantity += item.quantity
                    existing.save()
                else:
                    item.cart = cart
                    item.save()
            anon_cart.delete()
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    return cart


def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:6]
    bestsellers = Product.objects.filter(is_bestseller=True)[:6]
    categories = Category.objects.all()
    recent_reviews = Review.objects.select_related('product')[:4]
    
    context = {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'categories': categories,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'core/home.html', context)


def product_list(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'newest')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(tagline__icontains=query) |
            Q(description__icontains=query) |
            Q(material__icontains=query)
        )

    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except Exception:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except Exception:
            pass

    if sort == 'price-low':
        products = products.order_by('price')
    elif sort == 'price-high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    elif sort == 'bestseller':
        products = products.order_by('-is_bestseller', '-reviews_count')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'selected_category': selected_category,
        'query': query,
        'sort': sort,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'total_count': products.count(),
    }
    return render(request, 'core/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    reviews = product.reviews.all()

    if request.method == 'POST' and 'submit_review' in request.POST:
        user_name = request.POST.get('user_name', '').strip()
        comment = request.POST.get('comment', '').strip()
        try:
            rating = int(request.POST.get('rating', 5))
        except ValueError:
            rating = 5

        if user_name and comment:
            Review.objects.create(
                product=product,
                user_name=user_name,
                rating=min(max(rating, 1), 5),
                comment=comment
            )
            # update review count and recalculate average rating
            all_revs = product.reviews.all()
            avg = sum(r.rating for r in all_revs) / all_revs.count()
            product.rating = Decimal(f"{avg:.2f}")
            product.reviews_count = all_revs.count()
            product.save()
            messages.success(request, "Thank you! Your review has been published.")
            return redirect('product_detail', slug=product.slug)

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'core/product_detail.html', context)


def cart_view(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()

    subtotal = Decimal(str(cart.subtotal))
    discount = Decimal('0.00')

    coupon = request.session.get('coupon_code', '')
    if coupon == 'MUG10':
        discount = subtotal * Decimal('0.10')
    elif coupon == 'CERAMIC20':
        discount = subtotal * Decimal('0.20')

    # Free shipping over $50 threshold, otherwise $4.99
    if subtotal >= Decimal('50.00') or subtotal == Decimal('0.00'):
        shipping = Decimal('0.00')
    else:
        shipping = Decimal('4.99')

    total = max(Decimal('0.00'), subtotal - discount + shipping)

    if request.method == 'POST' and 'apply_coupon' in request.POST:
        code = request.POST.get('coupon_code', '').strip().upper()
        if code in ['MUG10', 'CERAMIC20']:
            request.session['coupon_code'] = code
            messages.success(request, f"Coupon '{code}' applied successfully!")
        else:
            messages.error(request, "Invalid coupon code. Try 'MUG10' or 'CERAMIC20'.")
        return redirect('cart_view')

    if request.method == 'POST' and 'remove_coupon' in request.POST:
        request.session.pop('coupon_code', None)
        messages.info(request, "Coupon removed.")
        return redirect('cart_view')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'discount': discount,
        'total': total,
        'coupon': coupon,
    }
    return render(request, 'core/cart.html', context)


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    qty = 1
    if request.method == 'POST':
        try:
            qty = max(1, int(request.POST.get('quantity', 1)))
        except ValueError:
            qty = 1
    custom_engraving = request.POST.get('custom_engraving', '').strip() if request.method == 'POST' else ''

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        custom_engraving=custom_engraving,
        defaults={'quantity': qty}
    )
    if not created:
        cart_item.quantity += qty
        cart_item.save()

    messages.success(request, f"Added {qty}x '{product.name}' to your cart!")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart_view'
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'cart_count': cart.total_items,
            'message': f"Added '{product.name}' to your cart!"
        })

    return redirect(next_url)


def cart_update(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    action = request.POST.get('action') or request.GET.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.info(request, f"Removed '{cart_item.product.name}' from your cart.")
            return redirect('cart_view')
    elif action == 'set':
        try:
            new_qty = int(request.POST.get('quantity', 1))
            if new_qty > 0:
                cart_item.quantity = new_qty
                cart_item.save()
            else:
                cart_item.delete()
        except ValueError:
            pass

    return redirect('cart_view')


def cart_remove(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f"Removed '{name}' from your cart.")
    return redirect('cart_view')


def checkout_view(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('product_list')

    subtotal = Decimal(str(cart.subtotal))
    discount = Decimal('0.00')
    coupon = request.session.get('coupon_code', '')
    if coupon == 'MUG10':
        discount = subtotal * Decimal('0.10')
    elif coupon == 'CERAMIC20':
        discount = subtotal * Decimal('0.20')

    shipping = Decimal('0.00') if subtotal >= Decimal('50.00') else Decimal('4.99')
    total = max(Decimal('0.00'), subtotal - discount + shipping)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')
        order_notes = request.POST.get('order_notes', '').strip()

        if not (full_name and email and phone and address and city and postal_code):
            messages.error(request, "Please fill in all required shipping fields.")
        else:
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code,
                payment_method=payment_method,
                subtotal=subtotal,
                shipping_fee=shipping,
                discount=discount,
                total=total,
                order_notes=order_notes,
                status='Processing'
            )

            # Create OrderItems and decrease stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    product_image=item.product.image_url,
                    price=item.product.effective_price,
                    quantity=item.quantity,
                    custom_engraving=item.custom_engraving
                )
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            # Clear cart and coupon
            cart.items.all().delete()
            request.session.pop('coupon_code', None)

            messages.success(request, f"Order #{order.order_number} confirmed! Thank you for supporting artisan pottery.")
            return redirect('order_confirmation', order_number=order.order_number)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'discount': discount,
        'total': total,
        'coupon': coupon,
    }
    return render(request, 'core/checkout.html', context)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    items = order.items.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'core/order_confirmation.html', context)


def track_order(request):
    order = None
    searched = False
    query = request.GET.get('order_number', '').strip()

    if query:
        searched = True
        order = Order.objects.filter(order_number__iexact=query).first()
        if not order:
            messages.error(request, f"No order found matching '{query}'. Please check the order number.")

    context = {
        'order': order,
        'searched': searched,
        'query': query,
    }
    return render(request, 'core/track_order.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        messages.success(request, f"Thank you, {name}! Your message has been received. Our ceramic artists will get back to you shortly.")
        return redirect('contact')
    return render(request, 'core/contact.html')
