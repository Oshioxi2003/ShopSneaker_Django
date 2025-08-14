#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShopSneaker.settings')
django.setup()

from store.models import Brand, Category, Size, Color, Product

def create_sample_data():
    print("Creating sample data...")
    
    # Create Brands
    nike, created = Brand.objects.get_or_create(
        name='Nike', 
        defaults={'slug': 'nike', 'is_active': True, 'description': 'Nike brand'}
    )
    if created:
        print("Created Nike brand")
    
    adidas, created = Brand.objects.get_or_create(
        name='Adidas',
        defaults={'slug': 'adidas', 'is_active': True, 'description': 'Adidas brand'}
    )
    if created:
        print("Created Adidas brand")
    
    # Create Categories
    running, created = Category.objects.get_or_create(
        name='Running',
        defaults={'slug': 'running', 'is_active': True, 'description': 'Running shoes'}
    )
    if created:
        print("Created Running category")
    
    casual, created = Category.objects.get_or_create(
        name='Casual',
        defaults={'slug': 'casual', 'is_active': True, 'description': 'Casual shoes'}
    )
    if created:
        print("Created Casual category")
    
    # Create Sizes
    for i in range(36, 44):
        size, created = Size.objects.get_or_create(name=str(i))
        if created:
            print(f"Created size {i}")
    
    # Create Colors
    colors_data = [
        ('White', '#FFFFFF'),
        ('Black', '#000000'), 
        ('Red', '#FF0000'),
        ('Blue', '#0000FF')
    ]
    
    for name, hex_code in colors_data:
        color, created = Color.objects.get_or_create(
            name=name,
            defaults={'hex_code': hex_code}
        )
        if created:
            print(f"Created color {name}")
    
    # Create Sample Products only if none exist
    if Product.objects.count() == 0:
        # Product 1
        product1 = Product.objects.create(
            title='Nike Air Max 270',
            slug='nike-air-max-270',
            brand=nike,
            category=running,
            original_price=150.00,
            sale_price=120.00,
            description='Comfortable running shoes with Air Max technology',
            short_description='Air Max running shoes',
            stock_quantity=50,
            is_featured=True,
            is_new=True,
            is_on_sale=True,
            status='active',
            tags='running, nike, air max'
        )
        print("Created Nike Air Max 270")
        
        # Product 2
        product2 = Product.objects.create(
            title='Adidas Ultraboost 22',
            slug='adidas-ultraboost-22',
            brand=adidas,
            category=running,
            original_price=180.00,
            description='Premium running shoes with Boost technology',
            short_description='Ultraboost running shoes',
            stock_quantity=30,
            is_featured=True,
            is_bestseller=True,
            status='active',
            tags='running, adidas, boost'
        )
        print("Created Adidas Ultraboost 22")
        
        # Product 3
        product3 = Product.objects.create(
            title='Nike Air Force 1',
            slug='nike-air-force-1',
            brand=nike,
            category=casual,
            original_price=100.00,
            description='Classic basketball shoe for everyday wear',
            short_description='Classic basketball shoe',
            stock_quantity=40,
            is_bestseller=True,
            status='active',
            tags='casual, nike, classic'
        )
        print("Created Nike Air Force 1")
        
        # Product 4
        product4 = Product.objects.create(
            title='Adidas Stan Smith',
            slug='adidas-stan-smith',
            brand=adidas,
            category=casual,
            original_price=80.00,
            sale_price=60.00,
            description='Iconic tennis shoe with minimalist design',
            short_description='Iconic tennis shoe',
            stock_quantity=35,
            is_on_sale=True,
            is_new=True,
            status='active',
            tags='casual, adidas, tennis'
        )
        print("Created Adidas Stan Smith")
        
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data() 