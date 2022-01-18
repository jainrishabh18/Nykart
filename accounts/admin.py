from django.contrib import admin
# 
from django.contrib.auth.admin import UserAdmin
from . models import Account

# Register your models here.

# with AccountAdmin we are changing the display how we want to see our admin page and what we want to be displayed
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name','username','last_login','date_joined','is_active')

    list_display_links=('email', 'first_name', 'last_name')
    
    readonly_fields =('last_login','date_joined')
    
    ordering =('-date_joined',)

    filter_horizontal =()
    list_filter =()
    fieldsets =()




admin.site.register(Account,AccountAdmin)
