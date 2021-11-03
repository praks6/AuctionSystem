from django.contrib import admin
from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    exclude = ('expire_date','is_expired' )


admin.site.register(Product, ProductAdmin)
