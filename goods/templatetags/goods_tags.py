from django import template
from django.utils.http import urlencode

from goods.models import Categories, Subcategories, Products
from goods.views import subcategories

register = template.Library()


@register.simple_tag()
def tag_all_categories():
    categories = Categories.objects.all()
    # if categories:
    all_categories = []
    for category in categories:
        subcategory = Subcategories.objects.filter(category_id=category.id)
        all_categories.append({'category': category, 'subcategory': subcategory})
    return all_categories
    # else:
    #     return None

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