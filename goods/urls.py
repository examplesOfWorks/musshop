from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('product/', views.product, name='product'),
    path('category/', views.categories, name='category'),
    path('subcategory/', views.subcategories, name='subcategory'),
]