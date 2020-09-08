from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import LoginForm, RegisterForm, UpdateForm, CustomPasswordChangeForm, DeleteUserForm, CustomPasswordResetForm, CustomPasswordSetForm
from core.utils import send_mail
from core.tokens import change_email_token, account_activation_token
from core.models import MailFromString
from orders.models import Order


User = get_user_model()


class LoginView(View):
    def post(self, request):
        login_form = LoginForm(request, request.POST)
        errors = login_form.non_field_errors()
        success = False

        if login_form.is_valid():
            if not login_form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            login(request, login_form.get_user())
            success = True

        context = {
            'success': success,
            'errors': errors,
        }

        return JsonResponse(context)


class RegisterView(View):
    def post(self, request):
        register_form = RegisterForm(request.POST)
        field_errors = register_form.errors.as_json()
        success = False
        email_error = None
        success_message = None

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False

            try:
                send_mail(request, user)
                user.save()
                success = True
                success_message = 'На указанную вами электронную почту выслано письмо с инструкциями для подтверждения учётной записи'
            except Exception as e:
                email_error = 'Ошибка! Перезагрузите страницу и попробуйте заново.'
                print(e)

        context = {
            'success': success,
            'errors': field_errors,
            'email_error': email_error,
            'success_message': success_message
        }

        return JsonResponse(context)


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64).decode())
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            context = {
                'msg': 'Аккаунт активирован',
                'text': 'Вы успешно подтвердили почту'
            }
            return render(request, 'users/activate.html', context)

        context = {
            'msg': 'Ошибка активации',
            'text': 'Ссылка на активацию недействительна'
        }
        return render(request, 'users/activate.html', context)


class LogoutView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        logout(request)
        return redirect('/')


class UserActiveOdersView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        user = request.user

        context = {
        }

        return render(request, 'users/user-orders-active.html', context)


class UserFinishedOdersView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):

        context = {
        }

        return render(request, 'users/user-orders-finished.html', context)


class OrderDetailView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, order_id):
        order = get_object_or_404(Order.objects.select_related('delivery', 'user'), pk=order_id, user=request.user)
        order_items = order.items.all().select_related('review', 'offer', 'offer__product')

        context = {
            'order': order,
            'order_items': order_items,
        }

        return render(request, 'users/order-detail.html', context)


class ProfileView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        user = request.user
        update_form = UpdateForm(instance=user, initial={'new_email': user.username})
        change_password_form = CustomPasswordChangeForm(user)
        delete_user_form = DeleteUserForm()

        context = {
            'update_form': update_form,
            'change_password_form': change_password_form,
            'delete_user_form': delete_user_form,
        }

        return render(request, 'users/profile.html', context)

    def post(self, request):
        user = request.user
        update_form = UpdateForm(request.POST, instance=user, initial={'new_email': user.username})
        delete_user_form = DeleteUserForm()
        change_password_form = CustomPasswordChangeForm(user)
        changed = False

        if update_form.has_changed():
            if update_form.is_valid():
                upd_user = update_form.save()
                if 'new_email' in update_form.changed_data:
                    send_mail(request, upd_user, register=False)

                    context = {
                        'msg': 'Проверьте почту',
                        'text': 'На указанную вами электронную почту выслано письмо с инструкциями для подтверждения учётной записи'
                    }

                    return render(request, 'users/activate.html', context)

                changed = True

        context = {
            'delete_user_form': delete_user_form,
            'change_password_form': change_password_form,
            'changed': changed,
            'update_form': update_form,
        }

        return render(request, 'users/profile.html', context)


class ChangeEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64).decode())
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and change_email_token.check_token(user, token):
            user.username = user.new_email
            user.new_email = None
            user.save()

            context = {
                'msg': 'Почта подтверждена',
                'text': 'Вы успешно подтвердили почту'
            }
            return render(request, 'users/activate.html', context)

        context = {
            'msg': 'Ошибка активации',
            'text': 'Ссылка на активацию недействительна'
        }
        return render(request, 'users/activate.html', context)


class ChangePasswordView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        user = request.user
        change_password_form = CustomPasswordChangeForm(user, request.POST)
        update_form = UpdateForm(instance=user, initial={'new_email': user.username})
        delete_user_form = DeleteUserForm()

        if change_password_form.is_valid():
            password = change_password_form.cleaned_data.get('new_password1')
            user.set_password(password)
            user.save()
            return redirect('/')

        context = {
            'delete_user_form': delete_user_form,
            'update_form': update_form,
            'change_password_form': change_password_form,
        }

        return render(request, 'users/profile.html', context)


class DeleteUserView(View):
    def get(self, request):
        return render(request, 'users/delete-user.html')

    def post(self, request):
        user = request.user
        success = False

        delete_user_form = DeleteUserForm(request, request.POST)
        errors = delete_user_form.non_field_errors()

        if delete_user_form.is_valid():
            user.is_active = False
            user.save()
            success = True

        context = {
            'success': success,
            'errors': errors
        }

        return JsonResponse(context) 


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password-reset.html'
    from_email = MailFromString.objects.first().host_user


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password-reset-done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordSetForm
    template_name = 'users/password-reset-confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password-reset-complete.html'
