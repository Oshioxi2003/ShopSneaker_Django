from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import (
    Category, Product, Size, Color, Brand, ProductVariant, 
    ProductImage, ProductReview, Wishlist, ProductView, DailyMetrics
)
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('sku', 'title', 'brand__name', 'category__name', 'original_price', 
                 'sale_price', 'stock_quantity', 'status', 'is_featured')

# Inline classes
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main', 'order']

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['size', 'color', 'stock_quantity', 'price_adjustment']

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ['user', 'rating', 'title', 'review', 'created_at']
    can_delete = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Số sản phẩm'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'product_count', 'website']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Số sản phẩm'

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'us_size', 'uk_size', 'eu_size']
    search_fields = ['name', 'us_size', 'uk_size', 'eu_size']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code', 'color_preview']
    search_fields = ['name', 'hex_code']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000; border-radius: 3px;"></div>',
            obj.hex_code
        )
    color_preview.short_description = 'Màu'

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = [
        'image_tag', 'sku', 'title', 'brand', 'category', 'price_display', 
        'stock_quantity', 'status', 'rating_display', 'is_featured', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'is_new', 'is_on_sale', 'is_bestseller',
        'brand', 'category', 'created_at'
    ]
    search_fields = ['title', 'sku', 'description', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['sku', 'created_at', 'updated_at', 'average_rating', 'review_count']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('sku', 'title', 'slug', 'description', 'short_description')
        }),
        ('Phân loại', {
            'fields': ('category', 'brand')
        }),
        ('Giá cả', {
            'fields': ('original_price', 'sale_price')
        }),
        ('Hình ảnh', {
            'fields': ('main_image',)
        }),
        ('Tồn kho & Trạng thái', {
            'fields': ('stock_quantity', 'min_stock_level', 'status')
        }),
        ('Thông số vật lý', {
            'fields': ('weight', 'length', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('SEO & Marketing', {
            'fields': ('meta_title', 'meta_description', 'tags'),
            'classes': ('collapse',)
        }),
        ('Cờ đặc biệt', {
            'fields': ('is_featured', 'is_new', 'is_on_sale', 'is_bestseller')
        }),
        ('Thống kê', {
            'fields': ('average_rating', 'review_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ProductImageInline, ProductVariantInline, ProductReviewInline]
    
    def image_tag(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 5px;"/>',
                obj.main_image.url
            )
        return "No Image"
    image_tag.short_description = 'Hình ảnh'
    
    def price_display(self, obj):
        if obj.sale_price:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">${}</span><br/>'
                '<span style="color: #e74c3c; font-weight: bold;">${}</span>',
                obj.original_price, obj.sale_price
            )
        return f"${obj.original_price}"
    price_display.short_description = 'Giá'
    
    def rating_display(self, obj):
        rating = obj.average_rating
        count = obj.review_count
        if rating > 0:
            stars = '★' * int(rating) + '☆' * (5 - int(rating))
            return format_html(
                '<span style="color: #f39c12;">{}</span> ({} đánh giá)',
                stars, count
            )
        return "Chưa có đánh giá"
    rating_display.short_description = 'Đánh giá'

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'stock_quantity', 'price_with_adjustment']
    list_filter = ['size', 'color', 'product__brand', 'product__category']
    search_fields = ['product__title', 'sku_variant']
    
    def price_with_adjustment(self, obj):
        return f"${obj.price}"
    price_with_adjustment.short_description = 'Giá (có điều chỉnh)'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_tag', 'is_main', 'order']
    list_filter = ['is_main', 'product__category']
    search_fields = ['product__title', 'alt_text']
    
    def image_tag(self, obj):
        return format_html(
            '<img src="{}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 5px;"/>',
            obj.image.url
        )
    image_tag.short_description = 'Hình ảnh'

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_approved', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_verified_purchase', 'created_at']
    search_fields = ['product__title', 'user__username', 'title', 'review']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"Đã duyệt {queryset.count()} đánh giá.")
    approve_reviews.short_description = "Duyệt các đánh giá đã chọn"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"Đã hủy duyệt {queryset.count()} đánh giá.")
    disapprove_reviews.short_description = "Hủy duyệt các đánh giá đã chọn"

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at', 'product__category']
    search_fields = ['user__username', 'product__title']

@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at', 'product__category']
    search_fields = ['product__title', 'user__username', 'ip_address']
    readonly_fields = ['created_at']

@admin.register(DailyMetrics)
class DailyMetricsAdmin(admin.ModelAdmin):
    list_display = ['date', 'money', 'users', 'sales', 'website_views']
    list_filter = ['date']
    readonly_fields = ['date']

# Admin site customization
admin.site.site_header = "ShopSneaker Admin"
admin.site.site_title = "ShopSneaker Admin Portal"
admin.site.index_title = "Chào mừng đến với ShopSneaker Administration"
