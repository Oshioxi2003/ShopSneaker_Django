
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Non-translatable URLs (like media files, API endpoints, etc.)
urlpatterns = [
    # Language switching
    path('i18n/', include('django.conf.urls.i18n')),
]

# Translatable URLs
urlpatterns += i18n_patterns(
    # Admin URL
    path('admin/', admin.site.urls),
    
    path('admin_shop/', include('admin_material.urls')),

    # Store app
    path('', include('store.urls')),

    # Cart app
    path('cart/', include('cart.urls')),

    # Account app
    path('account/', include('account.urls')),

    # Payment
    path('payment/', include('payment.urls')),
    
    prefix_default_language=True
)

# Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)