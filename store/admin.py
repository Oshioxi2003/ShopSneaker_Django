from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Size
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('image_tag', 'title', 'price', 'status')

    def image_tag(self, obj):
        return format_html('<img src="{}" style="height: 50px;"/>'.format(obj.image.url))
    image_tag.short_description = 'Image'

admin.site.register(Size)
