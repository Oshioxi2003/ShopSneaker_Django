from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (
    Category, Product, Brand, Size, Color, 
    ProductVariant, ProductReview, Wishlist, ProductView
)

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def store(request):
    """Enhanced store homepage with filters and search"""
    # Get filter parameters
    category_filter = request.GET.get('category')
    brand_filter = request.GET.get('brand')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', '-created_at')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    # Base queryset
    products = Product.objects.filter(status='active').select_related('category', 'brand')
    
    # Apply filters
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
    if brand_filter:
        products = products.filter(brand__slug=brand_filter)
    
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    if price_min:
        products = products.filter(original_price__gte=price_min)
    
    if price_max:
        products = products.filter(original_price__lte=price_max)
    
    # Sort products
    if sort_by == 'price_asc':
        products = products.order_by('original_price')
    elif sort_by == 'price_desc':
        products = products.order_by('-original_price')
    elif sort_by == 'name':
        products = products.order_by('title')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Featured products for homepage
    featured_products = Product.objects.filter(
        status='active', 
        is_featured=True
    ).select_related('category', 'brand')[:4]
    
    # New arrivals
    new_products = Product.objects.filter(
        status='active', 
        is_new=True
    ).select_related('category', 'brand')[:8]
    
    # Best sellers
    bestsellers = Product.objects.filter(
        status='active', 
        is_bestseller=True
    ).select_related('category', 'brand')[:4]
    
    # Get all brands for filter
    brands = Brand.objects.filter(is_active=True).annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)
    
    context = {
        'my_products': page_obj,
        'featured_products': featured_products,
        'new_products': new_products,
        'bestsellers': bestsellers,
        'brands': brands,
        'search_query': search_query,
        'current_category': category_filter,
        'current_brand': brand_filter,
        'sort_by': sort_by,
        'price_min': price_min,
        'price_max': price_max,
    }

    return render(request, 'store/store.html', context)

def categories(request):
    """Context processor for categories"""
    all_categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)
    return {'all_categories': all_categories}

def list_category(request, category_slug=None):
    """Enhanced category listing with filters"""
    category = get_object_or_404(Category, slug=category_slug)
    
    # Get filter parameters
    brand_filter = request.GET.get('brand')
    sort_by = request.GET.get('sort', '-created_at')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    # Base queryset
    products = Product.objects.filter(
        category=category, 
        status='active'
    ).select_related('brand')
    
    # Apply filters
    if brand_filter:
        products = products.filter(brand__slug=brand_filter)
    
    if price_min:
        products = products.filter(original_price__gte=price_min)
    
    if price_max:
        products = products.filter(original_price__lte=price_max)
    
    # Sort products
    if sort_by == 'price_asc':
        products = products.order_by('original_price')
    elif sort_by == 'price_desc':
        products = products.order_by('-original_price')
    elif sort_by == 'name':
        products = products.order_by('title')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get brands in this category
    brands = Brand.objects.filter(
        products__category=category,
        is_active=True
    ).distinct().annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)
    
    context = {
        'category': category,
        'products': page_obj,
        'brands': brands,
        'current_brand': brand_filter,
        'sort_by': sort_by,
        'price_min': price_min,
        'price_max': price_max,
    }
    
    return render(request, 'store/list-category.html', context)

def product_info(request, product_slug):
    """Enhanced product detail page"""
    product = get_object_or_404(Product, slug=product_slug, status='active')
    
    # Track product view
    ip_address = get_client_ip(request)
    ProductView.objects.create(
        product=product,
        user=request.user if request.user.is_authenticated else None,
        ip_address=ip_address
    )
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        status='active'
    ).exclude(id=product.id).select_related('brand')[:4]
    
    # Get product variants
    variants = ProductVariant.objects.filter(
        product=product
    ).select_related('size', 'color')
    
    # Get available sizes and colors
    available_sizes = Size.objects.filter(
        variants__product=product
    ).distinct().order_by('name')
    
    available_colors = Color.objects.filter(
        variants__product=product
    ).distinct().order_by('name')
    
    # Get product images
    product_images = product.images.all().order_by('order')
    
    # Get approved reviews
    reviews = ProductReview.objects.filter(
        product=product,
        is_approved=True
    ).select_related('user').order_by('-created_at')
    
    # Check if user has reviewed
    user_has_reviewed = False
    user_review = None
    if request.user.is_authenticated:
        user_review = ProductReview.objects.filter(
            product=product,
            user=request.user
        ).first()
        user_has_reviewed = user_review is not None
    
    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'variants': variants,
        'available_sizes': available_sizes,
        'available_colors': available_colors,
        'product_images': product_images,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
    }
    
    return render(request, 'store/product-info.html', context)

@login_required
@require_POST
def add_review(request, product_slug):
    """Add product review"""
    product = get_object_or_404(Product, slug=product_slug)
    
    # Check if user already reviewed
    if ProductReview.objects.filter(product=product, user=request.user).exists():
        messages.error(request, 'Bạn đã đánh giá sản phẩm này rồi.')
        return redirect('product-info', product_slug=product_slug)
    
    rating = request.POST.get('rating')
    title = request.POST.get('title')
    review_text = request.POST.get('review')
    
    if rating and title and review_text:
        ProductReview.objects.create(
            product=product,
            user=request.user,
            rating=int(rating),
            title=title,
            review=review_text,
            is_approved=True  # Auto-approve for now
        )
        messages.success(request, 'Cảm ơn bạn đã đánh giá sản phẩm!')
    else:
        messages.error(request, 'Vui lòng điền đầy đủ thông tin đánh giá.')
    
    return redirect('product-info', product_slug=product_slug)

@login_required
@require_POST
def toggle_wishlist(request, product_id):
    """Toggle product in wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        wishlist_item.delete()
        in_wishlist = False
        message = 'Đã xóa khỏi danh sách yêu thích'
    else:
        in_wishlist = True
        message = 'Đã thêm vào danh sách yêu thích'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'in_wishlist': in_wishlist,
            'message': message
        })
    
    messages.success(request, message)
    return redirect('product-info', product_slug=product.slug)

@login_required
def wishlist_view(request):
    """View user's wishlist"""
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('product__brand', 'product__category').order_by('-created_at')
    
    context = {
        'wishlist_items': wishlist_items
    }
    
    return render(request, 'store/wishlist.html', context)

def search_products(request):
    """AJAX product search"""
    query = request.GET.get('q', '')
    
    if len(query) >= 3:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(tags__icontains=query),
            status='active'
        ).select_related('brand')[:10]
        
        results = []
        for product in products:
            results.append({
                'id': product.id,
                'title': product.title,
                'brand': product.brand.name,
                'price': str(product.price),
                'image': product.main_image.url if product.main_image else '',
                'url': product.get_absolute_url()
            })
        
        return JsonResponse({'products': results})
    
    return JsonResponse({'products': []})

def get_variant_info(request, product_id):
    """Get variant information for AJAX"""
    size_id = request.GET.get('size')
    color_id = request.GET.get('color')
    
    if size_id and color_id:
        try:
            variant = ProductVariant.objects.get(
                product_id=product_id,
                size_id=size_id,
                color_id=color_id
            )
            return JsonResponse({
                'stock_quantity': variant.stock_quantity,
                'price': str(variant.price),
                'sku': variant.sku_variant,
                'available': variant.stock_quantity > 0
            })
        except ProductVariant.DoesNotExist:
            pass
    
    return JsonResponse({
        'stock_quantity': 0,
        'price': '0',
        'sku': '',
        'available': False
    })
    