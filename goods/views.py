from django.shortcuts import render

def catalog(request):
    context = {
        'title': 'Каталог',
    }
    return render(request, 'goods/catalog.html', context)

def product(request):
    context = {
        'title': 'Карточка товара',
    }
    return render(request, 'goods/product.html', context)

def categories(request):
    context = {
        'title': 'Категории',
    }
    return render(request, 'goods/category.html', context)

def subcategories(request):
    context = {
        'title': 'Подкатегории',
    }
    return render(request, 'goods/subcategory.html', context)