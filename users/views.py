from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import auth, messages

from users.forms import UserLoginForm, UserRegistrationForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username =  request.POST['username']
            password =  request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                redirect_page = request.POST.get('next', None)

                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserLoginForm()
        
    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            user = form.instance
            auth.login(request, user)

            messages.success(request, f"{user.username}, Вы успешно зарегистрировались и вошли в аккаунт")
            return HttpResponseRedirect(reverse('user:profile'))

    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form,  
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
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))
