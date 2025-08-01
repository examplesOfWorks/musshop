from django.contrib import admin
from users.models import User, Wishlist

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name', 'last_name', 'email',]
    search_fields = ['username','first_name', 'last_name', 'email',]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product',]