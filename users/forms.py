from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from users.models import User

class UserLoginForm(AuthenticationForm): #из AuthenticationForm. Просмотр содержания через F12

    class Meta: 
        model = User

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    phone_number = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()