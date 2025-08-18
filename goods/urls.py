from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/<slug:subcategory_slug>', views.catalog, name='search'),
    path('filter-products-by-type/', views.filter_products_by_type, name='filter_products_by_type'),
    path('<slug:subcategory_slug>', views.catalog, name='index'),
    path('product/<slug:product_article>', views.product, name='product'),
    path('categories/', views.categories, name='categories'),
    path('subcategories/<slug:category_slug>', views.subcategories, name='subcategories'),
    path('brands/', views.brands, name='brands'),
    path('brand/<slug:brand_slug>', views.brand, name='brand'),
]