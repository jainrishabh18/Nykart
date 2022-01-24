from django.contrib import admin
from .models import Product,Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','is_available','modified_date')
    prepopulated_fields={'slug' : ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    # editable can be edited  by just clicking on is_active in admin panel
    list_editable =('is_active',)
    # the list filter will show a side panel in django admin where we can choose products using filters.
    list_filter = ('product','variation_category','variation_value')
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)

