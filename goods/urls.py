from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/<slug:subcategory_slug>', views.CatalogView.as_view(), name='search'),
    path('filter-products-by-type/', views.TypeFilterView.as_view(), name='filter_products_by_type'),
    path('<slug:subcategory_slug>', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_article>', views.ProductView.as_view(), name='product'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('subcategories/<slug:category_slug>', views.SubcategoriesView.as_view(), name='subcategories'),
]