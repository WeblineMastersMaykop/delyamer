from django import forms
from contacts.models import FeedBack


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ('name', 'email_or_phone', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email_or_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон или E-mail'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст сообщения', 'rows': 4}),
        }