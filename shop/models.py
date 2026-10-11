from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    tagline = models.CharField(max_length=200, default="Brewed to be Wild • Non-Alcoholic")
    hero_headline = models.CharField(max_length=200, default="LOREM IPSUM CONSECTETUR DOLOR SIT CONSECT.")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=14.99)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=18.00)
    description = models.TextField(default="Crisp, refreshing craft soft drink engineered with premium botanicals, zero artificial colors, and an electric fizz that satisfies all day long.")
    flavor_notes = models.CharField(max_length=255, default="Smooth malt blend, zesty citrus peel, balanced sparkling finish")
    alcohol_vol = models.CharField(max_length=50, default="<0.5% NON-ALCOHOLIC")
    volume = models.CharField(max_length=50, default="12 FL. OZ. (355 ML)")
    calories = models.CharField(max_length=30, default="15 CAL")
    sugar = models.CharField(max_length=30, default="0g SUGAR")
    primary_color = models.CharField(max_length=30, default="#E5A812")
    image_url = models.CharField(max_length=255, default="/static/shop/images/hedlum_can_original.png")
    is_featured = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    review_count = models.PositiveIntegerField(default=128)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    session_key = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def qualifies_for_free_shipping(self):
        return self.total_price() >= 35.00

    def amount_needed_for_free_shipping(self):
        diff = 35.00 - float(self.total_price())
        return max(0.0, round(diff, 2))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pack_size = models.CharField(max_length=60, default="12-Pack Case")
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=14.99)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} ({self.pack_size})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Confirmed & Processing'),
        ('SHIPPED', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
    ]

    order_number = models.CharField(max_length=40, unique=True)
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=30)
    subtotal_amount = models.DecimalField(max_digits=8, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PAID')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=150)
    pack_size = models.CharField(max_length=60)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.unit_price * self.quantity
