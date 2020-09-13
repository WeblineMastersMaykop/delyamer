from django import forms
from orders.models import Order


class OrderOneClickForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control phone-input', 'placeholder': 'Номер телефона'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('postcode', 'country', 'region', 'city', 'address', 'phone', 'full_name', 'email', 'delivery')
        widgets = {
            'postcode': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Почтовый индекс'}),
            'country': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Страна'}),
            'region': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Регион'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Населённый пункт'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Адрес'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm phone-input', 'placeholder': 'Телефон'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ФИО'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Эл. почта'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
