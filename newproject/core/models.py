from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True, help_text="Short highlight, e.g., 'Handcrafted Matte Ceramic'")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Mug specific attributes
    capacity = models.CharField(max_length=50, default='350 ml (12 oz)', help_text="e.g., 350ml / 12oz, 450ml / 16oz")
    material = models.CharField(max_length=100, default='Stoneware Ceramic', help_text="Ceramic, Porcelain, Enamel, Stainless Steel")
    dimensions = models.CharField(max_length=100, default='9.5cm H x 8.5cm Dia')
    color = models.CharField(max_length=50, default='Natural Clay')
    dishwasher_safe = models.BooleanField(default=True)
    microwave_safe = models.BooleanField(default=True)
    allow_custom_engraving = models.BooleanField(default=True, help_text="Can customer add custom engraved text?")
    
    # Images & Media
    image_url = models.URLField(max_length=600)
    secondary_image_url = models.URLField(max_length=600, blank=True)
    
    # Inventory & Status
    stock = models.PositiveIntegerField(default=20)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.9)
    reviews_count = models.PositiveIntegerField(default=18)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.discount_price < self.price:
            savings = self.price - self.discount_price
            return int(round((savings / self.price) * 100))
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Cart(models.Model):
    session_key = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def free_shipping_threshold(self):
        return 50.00

    @property
    def free_shipping_remaining(self):
        rem = float(self.free_shipping_threshold) - float(self.subtotal)
        return max(0.0, rem)

    def __str__(self):
        return f"Cart #{self.id} ({self.session_key})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    custom_engraving = models.CharField(max_length=80, blank=True, help_text="Optional custom name or text")

    @property
    def total_price(self):
        return self.product.effective_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Cart #{self.cart_id})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit / Debit Card (Mock)'),
        ('bank', 'Direct Bank Transfer'),
    ]

    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Customer Details
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    
    # Order Financials
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='cod')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Processing')
    order_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"MUG-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} by {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    product_image = models.URLField(max_length=600, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    custom_engraving = models.CharField(max_length=80, blank=True)

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in {self.order.order_number}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user_name} on {self.product.name}"
