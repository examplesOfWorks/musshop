from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist-add/', views.wishlist_add, name='wishlist_add'),
    path('logout/', views.logout, name='logout'),
]