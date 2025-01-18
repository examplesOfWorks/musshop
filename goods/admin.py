from django.contrib import admin
from goods.models import Categories, Subcategories, Brands, Types, Products

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('name',)}
    list_display = ['name',]

@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('name',)}
    list_display = ['name',]
    list_filter = ['category']

@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('name',)}
    list_display = ['name',]

@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('name',)}
    list_display = ['name',]
    list_filter = ['subcategory']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('article',)}
    list_display = ['name', 'warranty', 'quantity', 'price', 'discount']
    list_editable = ['discount']
    search_fields = ['name', 'article', 'specifications','description']
    list_filter = ['discount', 'quantity', 'subcategory', 'brand', 'type']
    fields = [
        'name',
        'article',
        'subcategory',
        'type',
        'brand',
        'slug',
        'specifications',
        'description',
        'instructions',
        'warranty',
        'image',
        ('price', 'discount'),
        'quantity',
    ]