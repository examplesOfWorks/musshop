from email.mime import image
import re
from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Brands, Categories, Subcategories, Products, Types, Gallery

def catalog(request, subcategory_slug):
    subcategory = None
    subcategory_types = None
    brands = Brands.objects.all()

    if subcategory_slug == 'all':
        products = Products.objects.all()
    else:
        products = Products.objects.filter(subcategory__slug=subcategory_slug)
        subcategory = Subcategories.objects.filter(slug=subcategory_slug)[0]
        subcategory_types = Types.objects.filter(subcategory__slug=subcategory_slug)

    context = {
    'title': 'Каталог',
    'products': products,
    'subcategory': subcategory,
    'subcategory_types': subcategory_types,
    'brands': brands,
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_article):
    product = Products.objects.get(article=product_article)
    specifications = product.specifications.split(';')
    images = product.images.all()[1:]

    # sp = []
    # for spec in specifications:
    #     s = spec.split(':')
    #     if spec:
    #         sp.append(s)

    # n = 1
    # sp = [specifications[i] for i in range(0, len(specifications), n)]

    context = {
        'title': 'Карточка товара',
        'product': product,
        'specifications': specifications,
        'images': images,
    }
    return render(request, 'goods/product.html', context)

def categories(request, category_slug):
    category = Categories.objects.get(slug=category_slug)
    subcategories = Subcategories.objects.filter(category_id=category.id)
    title = category.name
    
    context = {
        'title': title,
        'category': category,
        'subcategories': subcategories,
    }
    return render(request, 'goods/category.html', context)

def subcategories(request):
    context = {
        'title': 'Подкатегории',
    }
    return render(request, 'goods/subcategory.html', context)