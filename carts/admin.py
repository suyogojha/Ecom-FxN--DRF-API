from django.contrib import admin
from carts.models import Cart, CartItem 


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display =  ('card_id', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
    list_display =  ('product', 'cart', 'quantity', 'is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
