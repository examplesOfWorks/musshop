from django.shortcuts import render

def login(request):
    context = {
        'title': 'Авторизация',
    }
    return render(request, 'users/login.html', context)

def registration(request):
    context = {
        'title': 'Регистрация',
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {
        'title': 'Профиль пользователя',
    }
    return render(request, 'users/profile.html', context)

def users_cart(request):
    context = {
        'title': 'Корзина',
    }
    return render(request, 'users/users_cart.html', context)

def wishlist(request):
    context = {
        'title': 'Избранное',
    }
    return render(request, 'users/wishlist.html', context)

def logout(request):
    pass
