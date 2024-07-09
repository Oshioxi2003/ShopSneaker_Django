
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    #admin url
    path('admin/', admin.site.urls),

    path('admin_shop/', include('admin_material.urls')),

    #Store app
    path('', include('store.urls')),

    #Cart app
    path('cart/', include('cart.urls')),

    #Account app

    path('account/', include('account.urls')),

    #payment

    path('payment/', include('payment.urls')),

    # admin-shop








]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)