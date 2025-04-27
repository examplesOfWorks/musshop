from django.db.models import Q

from goods.models import Products
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
# from goods.views import brand

def filter_by_brand(all_brands, products):
    q_objects = Q()
    for brand in all_brands:
        q_objects |= Q(brand__slug=brand)
    return products.filter(q_objects)

def q_search(query):
    # if len(query) == 6:
    # print(query)
    if len(query) == 7 and query[1::].isdigit():
        result = Products.objects.filter(article=query)
        result = result.annotate(
        skuline=SearchHeadline(
            "article",
            query,
            start_sel='<span style="background-color: #3474d4; color: #ffffff; padding: 2px">',
            stop_sel='</span>',
        ),
    )
        return result

    
    vector = SearchVector("name", "description", "specifications")
    query = SearchQuery(query)

    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: #3474d4; color: #ffffff; padding: 2px;">',
            stop_sel='</span>',
        ),
    )

    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: #3474d4; color: #ffffff; padding: 2px">',
            stop_sel='</span>',
        ),
    )
    return result

