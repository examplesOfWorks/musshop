from django.contrib import admin
from goods.models import Categories, Subcategories, Brands, Types, Products, Gallery

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


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_timestamp',)
    list_display = ['name', 'warranty', 'quantity', 'price', 'discount']
    list_editable = ['discount']
    search_fields = ['name', 'article', 'specifications','description']
    list_filter = ['discount', 'created_timestamp', 'subcategory', 'brand', 'type']
    inlines = [GalleryInline,]
    fields = [
        'name',
        'article',
        'subcategory',
        'type',
        'brand',
        'specifications',
        'description',
        # 'instructions',
        'warranty',
        ('price', 'discount'),
        'quantity',
        'created_timestamp',
    ]
