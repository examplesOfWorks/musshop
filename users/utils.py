from users.models import Wishlist

def get_wishlist_count(request):
    if request.user.is_authenticated:
        return Wishlist.objects.filter(user=request.user).count()
    else:
        return 0
    
def get_user_wishlist(request):
    if request.user.is_authenticated:
        return Wishlist.objects.filter(user=request.user).order_by('-created_timestamp')
    else:
        return 0