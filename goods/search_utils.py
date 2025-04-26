from django.db.models import Q

# from goods.models import Brands
# from goods.views import brand

def filter_by_brand(all_brands, products):
    q_objects = Q()
    for brand in all_brands:
        q_objects |= Q(brand__slug=brand)
    return products.filter(q_objects)

