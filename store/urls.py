from django.urls import path

from . import views

urlpatterns= [
    #store main page
    path('', views.store, name='store'),

    #Indivadual product
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),

    #indivadual categopry
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),


]
