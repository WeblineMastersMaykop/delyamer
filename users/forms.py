from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
    PasswordResetForm, SetPasswordForm,
    PasswordChangeForm, AuthenticationForm,
    UserCreationForm, PasswordResetForm,
    SetPasswordForm, PasswordChangeForm
)


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'CheckKeepSignIn'}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'}))
    password1 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('postcode', 'country', 'region', 'city', 'address', 'phone', 'full_name', 'new_email')
        widgets = {
            'postcode': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Почтовый индекс'}),
            'country': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Страна'}),
            'region': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Регион'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Населённый пункт'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Адрес'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm phone-input', 'placeholder': 'Телефон'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'ФИО'}),
            'new_email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Эл. почта'})
        }

    def clean_new_email(self):
        username = self.cleaned_data.get('new_email')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует')
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует')
        return phone


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Повторите новый пароль'}))


class CustomPasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите новый пароля'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтной не найден')

        return email

    # def send_mail(self, subject_template_name, email_template_name,
    #               context, from_email, to_email, html_email_template_name=None):
    #     subject = loader.render_to_string(subject_template_name, context)
    #     subject = ''.join(subject.splitlines())
    #     body = loader.render_to_string(email_template_name, context)

    #     from_email = MailFromString.objects.first().host_user

    #     email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    #     if html_email_template_name is not None:
    #         html_email = loader.render_to_string(html_email_template_name, context)
    #         email_message.attach_alternative(html_email, 'text/html')
    #     email_message.send()


class DeleteUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.request.user != self.user_cache:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
