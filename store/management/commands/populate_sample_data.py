from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Category, Brand, Size, Color, Product, ProductVariant
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Categories
        categories_data = [
            {'name': 'Running Shoes', 'slug': 'running-shoes'},
            {'name': 'Basketball', 'slug': 'basketball'},
            {'name': 'Casual', 'slug': 'casual'},
            {'name': 'Lifestyle', 'slug': 'lifestyle'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': f'{cat_data["name"]} collection',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create Brands
        brands_data = [
            {'name': 'Nike', 'slug': 'nike'},
            {'name': 'Adidas', 'slug': 'adidas'},
            {'name': 'Jordan', 'slug': 'jordan'},
            {'name': 'Puma', 'slug': 'puma'},
            {'name': 'Converse', 'slug': 'converse'},
        ]
        
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                slug=brand_data['slug'],
                defaults={
                    'name': brand_data['name'],
                    'description': f'{brand_data["name"]} brand',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created brand: {brand.name}')
        
        # Create Sizes
        sizes_data = [
            {'name': '36', 'us_size': '5', 'uk_size': '3', 'eu_size': '36'},
            {'name': '37', 'us_size': '6', 'uk_size': '4', 'eu_size': '37'},
            {'name': '38', 'us_size': '7', 'uk_size': '5', 'eu_size': '38'},
            {'name': '39', 'us_size': '8', 'uk_size': '6', 'eu_size': '39'},
            {'name': '40', 'us_size': '9', 'uk_size': '7', 'eu_size': '40'},
            {'name': '41', 'us_size': '10', 'uk_size': '8', 'eu_size': '41'},
            {'name': '42', 'us_size': '11', 'uk_size': '9', 'eu_size': '42'},
            {'name': '43', 'us_size': '12', 'uk_size': '10', 'eu_size': '43'},
        ]
        
        for size_data in sizes_data:
            size, created = Size.objects.get_or_create(
                name=size_data['name'],
                defaults=size_data
            )
            if created:
                self.stdout.write(f'Created size: {size.name}')
        
        # Create Colors
        colors_data = [
            {'name': 'White', 'hex_code': '#FFFFFF'},
            {'name': 'Black', 'hex_code': '#000000'},
            {'name': 'Red', 'hex_code': '#FF0000'},
            {'name': 'Blue', 'hex_code': '#0000FF'},
            {'name': 'Green', 'hex_code': '#00FF00'},
            {'name': 'Gray', 'hex_code': '#808080'},
            {'name': 'Navy', 'hex_code': '#000080'},
            {'name': 'Brown', 'hex_code': '#A52A2A'},
        ]
        
        for color_data in colors_data:
            color, created = Color.objects.get_or_create(
                name=color_data['name'],
                defaults=color_data
            )
            if created:
                self.stdout.write(f'Created color: {color.name}')
        
        # Create Sample Products
        products_data = [
            {
                'title': 'Air Max 270 React',
                'slug': 'air-max-270-react',
                'brand': 'Nike',
                'category': 'Running Shoes',
                'original_price': 150.00,
                'sale_price': 120.00,
                'description': 'Experience unparalleled comfort with Nike Air Max 270 React',
                'short_description': 'Comfortable running shoes with React technology',
                'is_featured': True,
                'is_new': True,
                'is_on_sale': True,
                'stock_quantity': 50,
                'tags': 'running, comfort, nike, air max'
            },
            {
                'title': 'UltraBoost 22',
                'slug': 'ultraboost-22',
                'brand': 'Adidas',
                'category': 'Running Shoes',
                'original_price': 180.00,
                'description': 'Adidas UltraBoost with Boost technology for maximum energy return',
                'short_description': 'Energy-returning running shoes',
                'is_featured': True,
                'is_bestseller': True,
                'stock_quantity': 30,
                'tags': 'running, boost, adidas, energy'
            },
            {
                'title': 'Jordan 1 Retro High OG',
                'slug': 'jordan-1-retro-high-og',
                'brand': 'Jordan',
                'category': 'Basketball',
                'original_price': 170.00,
                'description': 'Classic Jordan 1 design with premium materials',
                'short_description': 'Iconic basketball shoes',
                'is_featured': True,
                'is_new': True,
                'stock_quantity': 25,
                'tags': 'basketball, jordan, retro, classic'
            },
            {
                'title': 'Suede Classic XXI',
                'slug': 'suede-classic-xxi',
                'brand': 'Puma',
                'category': 'Casual',
                'original_price': 70.00,
                'description': 'Timeless Puma Suede design updated for modern style',
                'short_description': 'Classic suede sneakers',
                'is_bestseller': True,
                'stock_quantity': 40,
                'tags': 'casual, suede, puma, classic'
            },
            {
                'title': 'Chuck Taylor All Star',
                'slug': 'chuck-taylor-all-star',
                'brand': 'Converse',
                'category': 'Lifestyle',
                'original_price': 60.00,
                'sale_price': 45.00,
                'description': 'Iconic Converse Chuck Taylor All Star sneakers',
                'short_description': 'Timeless canvas sneakers',
                'is_on_sale': True,
                'stock_quantity': 60,
                'tags': 'lifestyle, canvas, converse, iconic'
            },
        ]
        
        # Use default image from static
        default_image_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'images', 'shoe.jpg')
        
        for product_data in products_data:
            try:
                brand = Brand.objects.get(name=product_data['brand'])
                category = Category.objects.get(name=product_data['category'])
                
                product, created = Product.objects.get_or_create(
                    slug=product_data['slug'],
                    defaults={
                        'title': product_data['title'],
                        'brand': brand,
                        'category': category,
                        'original_price': product_data['original_price'],
                        'sale_price': product_data.get('sale_price'),
                        'description': product_data['description'],
                        'short_description': product_data['short_description'],
                        'is_featured': product_data.get('is_featured', False),
                        'is_new': product_data.get('is_new', False),
                        'is_on_sale': product_data.get('is_on_sale', False),
                        'is_bestseller': product_data.get('is_bestseller', False),
                        'stock_quantity': product_data['stock_quantity'],
                        'tags': product_data['tags'],
                        'status': 'active'
                    }
                )
                
                if created:
                    # Try to copy default image if exists
                    if os.path.exists(default_image_path):
                        with open(default_image_path, 'rb') as f:
                            image_content = f.read()
                            product.main_image.save(
                                f'{product.slug}.jpg',
                                ContentFile(image_content),
                                save=True
                            )
                    
                    self.stdout.write(f'Created product: {product.title}')
                    
                    # Create some variants
                    sizes = Size.objects.all()[:4]  # Get first 4 sizes
                    colors = Color.objects.all()[:3]  # Get first 3 colors
                    
                    for size in sizes:
                        for color in colors:
                            variant, created = ProductVariant.objects.get_or_create(
                                product=product,
                                size=size,
                                color=color,
                                defaults={
                                    'sku_variant': f'{product.sku}-{size.name}-{color.name}',
                                    'stock_quantity': 10,
                                    'price_adjustment': 0
                                }
                            )
                            if created:
                                self.stdout.write(f'  Created variant: {variant.sku_variant}')
                
            except Exception as e:
                self.stdout.write(f'Error creating product {product_data["title"]}: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!')) 