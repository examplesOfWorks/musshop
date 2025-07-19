from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth, messages

from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

from orders.phone_utils import format_phone, clean_phone

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username =  request.POST['username']
            password =  request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key=request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if session_key:
                    new_carts = Cart.objects.filter(session_key=session_key)
                    old_carts = Cart.objects.filter(user=user)
                    products_from_new_carts = new_carts.values_list('product_id', flat=True)

                    for product_id in products_from_new_carts:
                        new_cart = new_carts.filter(product_id=product_id)
                        forgot_cart =  old_carts.filter(product_id=product_id)

                        new_quantity = new_cart.aggregate(Sum('quantity'))
                        old_quantity = forgot_cart.aggregate(Sum('quantity'))

                        if not old_quantity['quantity__sum']:
                            old_quantity['quantity__sum'] = 0
                        if not new_quantity['quantity__sum']:
                            new_quantity['quantity__sum'] = 0

                        quantity = new_quantity['quantity__sum'] + old_quantity['quantity__sum']

                        if new_cart.exists() and forgot_cart.exists():
                            forgot_cart.delete()

                        new_cart.update(user=user, session_key=None, quantity=quantity)

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

            session_key=request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f"{user.username}, Вы успешно зарегистрировались и вошли в аккаунт")
            return HttpResponseRedirect(reverse('user:profile'))

    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form,  
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    user = request.user
    initial = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone_number': format_phone(user.phone_number or ''),
    }
    form = UserUpdateForm(initial=initial)

    context = {
        'title': 'Профиль пользователя',
        'body_class': 'shop_page',
        'form': form
    }
    return render(request, 'users/profile.html', context)

@login_required
def update_profile(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        post_data = request.POST.copy()

        phone = post_data.get('phone_number', '')
        post_data['phone_number'] = clean_phone(phone)

        form = UserUpdateForm(post_data, instance=request.user)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Недопустимый запрос'}, status=400)

def users_cart(request):
    context = {
        'title': 'Корзина',
        'show_btn': True,
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
