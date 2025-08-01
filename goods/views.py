from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Brands, Categories, Subcategories, Products, Types, Gallery
from goods.search_utils import filter_by_brand, q_search 

def catalog(request, subcategory_slug):
    subcategory = None
    subcategory_types = None
    on_sale = request.GET.get('discount', None)
    all_brands = request.GET.getlist('brand', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if request.user.is_authenticated:
        wishlist_product_ids = set(
            request.user.wishlist_items.values_list("product_id", flat=True)
        )
    else:
        wishlist_product_ids = set()

    if subcategory_slug == 'all':
        products = Products.objects.all()
        brands = Brands.objects.all()
    # elif query:
    #     products = q_search(query)
    #     brands = Brands.objects.all()
    else:
        products = Products.objects.filter(subcategory__slug=subcategory_slug)
        subcategory = Subcategories.objects.filter(slug=subcategory_slug)[0]
        subcategory_types = Types.objects.filter(subcategory__slug=subcategory_slug)
        brands = Brands.objects.filter(products__in=products)

    if on_sale:
        products = products.filter(discount__gt=0)

    if all_brands:
        products = filter_by_brand(all_brands, products)

    if order_by and order_by != "default":
        products = products.order_by(order_by)
    
    if query:
        products = q_search(query)
        brands = Brands.objects.all()
    
    context = {
    'title': 'Каталог',
    'products': products,
    'subcategory': subcategory,
    'subcategory_types': subcategory_types,
    'brands': brands,
    'all_brands': all_brands,
    'subcategory_slug': subcategory_slug,
    'wishlist_product_ids': wishlist_product_ids
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_article):
    product = Products.objects.get(article=product_article)
    specifications = product.specifications.split(';')
    images = product.images.all()[1:]

    in_wishlist = request.user.wishlist_items.filter(product_id=product.id).exists()

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
        'in_wishlist': in_wishlist
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

def brands(request):
    brands = Brands.objects.all()
    context = {
        'title': 'Бренды',
        'brands': brands,
    }
    return render(request, 'goods/brands.html', context)

def brand(request, brand_slug):
    brand = Brands.objects.get(slug=brand_slug)
    context = {
        'title': brand.name,
        'brand': brand,
    }
    return render(request, 'goods/brand.html', context)