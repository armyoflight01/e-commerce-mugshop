from .models import Cart, Category


def cart_context(request):
    """Provides cart summary and product categories across all templates."""
    total_qty = 0
    subtotal = 0.0

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if not cart and session_key:
                cart = Cart.objects.filter(session_key=session_key).first()
        else:
            cart = Cart.objects.filter(session_key=session_key).first()

        if cart:
            total_qty = cart.total_items
            subtotal = float(cart.subtotal)
    except Exception:
        total_qty = 0
        subtotal = 0.0

    categories = Category.objects.all()

    return {
        'cart_count': total_qty,
        'cart_subtotal': subtotal,
        'nav_categories': categories,
    }
