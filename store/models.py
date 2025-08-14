from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

# Create your models here.

class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)
    us_size = models.CharField(max_length=10, blank=True, null=True)
    uk_size = models.CharField(max_length=10, blank=True, null=True)
    eu_size = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'sizes'
        ordering = ['name']

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, help_text="Color hex code (e.g., #FF0000)")
    
    class Meta:
        verbose_name_plural = 'colors'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'brands'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Còn hàng'),
        ('out_of_stock', 'Hết hàng'),
        ('discontinued', 'Ngừng kinh doanh'),
        ('coming_soon', 'Sắp ra mắt'),
    ]
    
    # Basic Information
    sku = models.CharField(max_length=100, unique=True, help_text="Stock Keeping Unit")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)
    
    # Relationships
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size, related_name='products', through='ProductVariant')
    colors = models.ManyToManyField(Color, related_name='products', through='ProductVariant')
    
    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Physical Properties
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Length in cm")
    width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Width in cm")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Height in cm")
    
    # Stock and Status
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5, help_text="Minimum stock level for alerts")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # SEO and Marketing
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    # Flags
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Main product image
    main_image = models.ImageField(upload_to='products/')

    class Meta:
        verbose_name_plural = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['category', 'brand']),
        ]

    def __str__(self):
        return self.title
    
    @property
    def price(self):
        """Return sale price if available, otherwise original price"""
        return self.sale_price if self.sale_price else self.original_price
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.sale_price and self.sale_price < self.original_price:
            return round(((self.original_price - self.sale_price) / self.original_price) * 100)
        return 0
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock_quantity > 0 and self.status == 'active'
    
    @property
    def is_low_stock(self):
        """Check if product stock is low"""
        return self.stock_quantity <= self.min_stock_level
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0
    
    @property
    def review_count(self):
        """Count approved reviews"""
        return self.reviews.filter(is_approved=True).count()

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class ProductVariant(models.Model):
    """Product variants for different size and color combinations"""
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    sku_variant = models.CharField(max_length=100, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    price_adjustment = models.DecimalField(max_digits=6, decimal_places=2, default=0, 
                                         help_text="Price adjustment for this variant")
    
    class Meta:
        unique_together = ['product', 'size', 'color']
        verbose_name_plural = 'product variants'
    
    def __str__(self):
        return f"{self.product.title} - {self.size.name} - {self.color.name}"
    
    @property
    def price(self):
        """Calculate variant price with adjustment"""
        base_price = self.product.price
        return base_price + self.price_adjustment

class ProductImage(models.Model):
    """Additional product images"""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'product images'
    
    def __str__(self):
        return f"{self.product.title} - Image {self.order}"

class ProductReview(models.Model):
    """Product reviews and ratings"""
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    review = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']
        verbose_name_plural = 'product reviews'
    
    def __str__(self):
        return f"{self.product.title} - {self.rating} stars by {self.user.username}"

class Wishlist(models.Model):
    """User wishlist for products"""
    user = models.ForeignKey(User, related_name='wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlisted_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product']
        verbose_name_plural = 'wishlists'
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class ProductView(models.Model):
    """Track product views for analytics"""
    product = models.ForeignKey(Product, related_name='views', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='viewed_products', on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'product views'
        indexes = [
            models.Index(fields=['product', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.product.title} viewed at {self.created_at}"

# Keep the existing DailyMetrics model
class DailyMetrics(models.Model):
    date = models.DateField(auto_now_add=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    users = models.IntegerField()
    new_clients = models.IntegerField()
    sales = models.DecimalField(max_digits=10, decimal_places=2)
    website_views = models.IntegerField()
    daily_sales = models.DecimalField(max_digits=10, decimal_places=2)
    completed_tasks = models.IntegerField()

    def __str__(self):
        return f"Metrics for {self.date}"