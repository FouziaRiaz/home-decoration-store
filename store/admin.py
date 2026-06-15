from django.contrib import admin
from .models import *
from .models import Product, Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display =('category_name','slug')
  

class ProductAdmin(admin.ModelAdmin):
    list_display =('id','name','price','category','is_available')
    prepopulated_fields = {'slug':('name',)}



admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
