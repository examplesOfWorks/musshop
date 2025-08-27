from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('users-cart/', views.UsersCartView.as_view(), name='users_cart'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist-add/', views.WishlistAddView.as_view(), name='wishlist_add'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]