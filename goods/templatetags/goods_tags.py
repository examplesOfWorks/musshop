from django import template
from django.db.models import Count
from django.utils.http import urlencode

from goods.models import Brands, Categories, Subcategories, Products

register = template.Library()


@register.simple_tag()
def tag_all_categories():
    categories = Categories.objects.all()
    all_categories = []
    for category in categories:
        subcategory = Subcategories.objects.filter(category_id=category.id)
        all_categories.append({'category': category, 'subcategory': subcategory})
    return all_categories

@register.simple_tag()
def products_count_category(category):
    return Products.objects.filter(subcategory__category=category).count()

@register.simple_tag()
def products_count_subcategory(subcategory):
    return Products.objects.filter(subcategory=subcategory).count()

@register.simple_tag()
def products_count_type(type):
    return Products.objects.filter(type=type).count()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.simple_tag()
def slider_products():
    top_products = Products.objects.filter(discount__gt=20).order_by('quantity')[:4]
    return top_products

@register.simple_tag()
def new_arrivals():
    new_products = Products.objects.filter(discount__gt=0).order_by('-created_timestamp')[:4]
    return new_products

@register.simple_tag()
def top_brands():
    brands = Brands.objects.filter(image__isnull=False).exclude(image="").annotate(product_count=Count('products')).filter(product_count__gt=0).order_by('-product_count')[:10]
    return brands