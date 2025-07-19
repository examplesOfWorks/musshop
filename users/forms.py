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

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        digits = ''.join(filter(str.isdigit, phone))
        if digits.startswith(('7', '8')):
            digits = digits[1:]
        return f'+7{digits}'
    
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