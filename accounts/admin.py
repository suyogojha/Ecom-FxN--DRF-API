from django.contrib import admin
from accounts.models import Account
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'is_active', 'is_staff')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('email', 'username',)
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)