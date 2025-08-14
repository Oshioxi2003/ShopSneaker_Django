from django.urls import path

from . import views

urlpatterns = [
    # Store main page
    path('', views.store, name='store'),

    # Individual product
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),

    # Individual category
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),
    
    # Product reviews
    path('product/<slug:product_slug>/review/', views.add_review, name='add-review'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle-wishlist'),
    
    # Search and filters
    path('search/products/', views.search_products, name='search-products'),
    path('product/<int:product_id>/variant-info/', views.get_variant_info, name='variant-info'),
]
