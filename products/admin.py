from django.contrib import admin
from .models import *

admin.site.register(category)
admin.site.register(Coupon)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImageAdmin]
    
    
@admin.register(colorvariant)
class colorvariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = colorvariant

@admin.register(sizevariant)
class sizevariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    model = sizevariant    

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)
