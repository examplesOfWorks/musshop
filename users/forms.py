from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.forms import fields

from users.models import User

from common.filters import clean_phone

class UserLoginForm(AuthenticationForm):

    class Meta: 
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()

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

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')
        return clean_phone(phone_number)
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
        )

    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    username = forms.CharField(label="Логин")
    email = forms.CharField(label="Email")
    phone_number = forms.CharField(label="Номер телефона")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')
        return clean_phone(phone_number)