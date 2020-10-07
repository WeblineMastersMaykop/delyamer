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
        fields = ('postcode', 'country', 'region', 'city', 'phone', 'full_name', 'email', 'delivery',
                  'micro_district', 'street', 'house_nmb', 'building_nmb', 'room_nmb')
        widgets = {
            'postcode': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Почтовый индекс*'}),
            'country': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Страна*'}),
            'region': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Регион*'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Населённый пункт*'}),
            'micro_district': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Микрорайон'}),
            'street': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Улица*'}),
            'house_nmb': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Номер дома*'}),
            'building_nmb': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Корпус'}),
            'room_nmb': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Квартира (офис)*'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm phone-input', 'placeholder': 'Телефон*'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ФИО*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Эл. почта*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            if key not in ('building_nmb', 'micro_district'):
                self.fields[key].required = True
