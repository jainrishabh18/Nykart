from django.contrib import admin
# 
from .models import Category


# Register your models here.

# cateogory admin is taking access to the category model and making changes to it according to developer requirements

class CategoryAdmin(admin.ModelAdmin):
    # here category name will automatically be added to slug field with help of prepoulated field
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display =('category_name','slug')


admin.site.register(Category,CategoryAdmin)