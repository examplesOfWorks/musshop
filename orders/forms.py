from django import forms

from orders.models import DeliveryMethod

class UserInfoForm(forms.Form):
    first_name = forms.CharField(label='Имя*')
    last_name = forms.CharField(label='Фамилия*')
    phone_number = forms.CharField(label='Номер телефона*')
    email = forms.EmailField(label='Email*')

class DeliveryForm(forms.Form):
    delivery_method = forms.ModelChoiceField(
        queryset=DeliveryMethod.objects.none(),
        widget=forms.RadioSelect,
    )
    delivery_address = forms.CharField(label='Адрес доставки', required=False)
    delivery_comment = forms.CharField(label='Комментарии к доставке', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = self.fields['delivery_method'].queryset = DeliveryMethod.objects.filter(is_active=True)

        try:
            pickup_option = queryset.get(name__iexact='Самовывоз')
            self.fields['delivery_method'].initial = pickup_option
        except DeliveryMethod.DoesNotExist:
            pass

    def clean(self):
        cleaned_data = super().clean()

        delivery_method = cleaned_data.get("delivery_method")
        delivery_address = cleaned_data.get("delivery_address")

        if delivery_method and delivery_method.price > 0 and not delivery_address:
            self.add_error("delivery_address", "Укажите адрес доставки.")

class PaymentForm(forms.Form):
    payment_on_get = forms.ChoiceField(choices=[
            ("0", False),
            ("1", True),
        ],
        initial="0",
        widget=forms.RadioSelect
    )
