from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    # path('search/', views.catalog, name='search'),
    path('search/<slug:subcategory_slug>', views.catalog, name='search'),
    path('<slug:subcategory_slug>', views.catalog, name='index'),
    path('product/<slug:product_article>', views.product, name='product'),
    path('category/<slug:category_slug>', views.categories, name='category'),
    path('subcategory/', views.subcategories, name='subcategory'),
    path('brands/', views.brands, name='brands'),
    path('brand/<slug:brand_slug>', views.brand, name='brand'),
]