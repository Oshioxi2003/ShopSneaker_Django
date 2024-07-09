from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Resource classes
class ShippingAddressResource(resources.ModelResource):
    class Meta:
        model = ShippingAddress

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order

class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem

# Admin classes
@admin.register(ShippingAddress)
class ShippingAddressAdmin(ImportExportModelAdmin):
    resource_class = ShippingAddressResource
    list_display = ('user', 'full_name', 'email', 'address1', 'city', 'state', 'zipcode')

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ('full_name', 'email', 'shipping_address', 'amount_paid', 'user')

@admin.register(OrderItem)
class OrderItemAdmin(ImportExportModelAdmin):
    resource_class = OrderItemResource
    list_display = ('order', 'product', 'quantity', 'price', 'get_username')

    def get_username(self, obj):
        return obj.user.username if obj.user else 'Anonymous'
    get_username.short_description = 'Username'
