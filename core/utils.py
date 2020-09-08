from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from core.tokens import account_activation_token, change_email_token
from core.models import MailFromString


def send_mail(request, user, register=True):
    current_site = get_current_site(request)
    subject = 'Подтверждение почты'

    if register:
        token = account_activation_token.make_token(user)
        template = 'users/activate-message.html'
        to_email = user.username
    else:
        token = change_email_token.make_token(user)
        template = 'users/change-email-message.html'
        to_email = user.new_email

    message = render_to_string(template, {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })

    from_email = MailFromString.objects.first().host_user
    email = EmailMessage(subject, message, from_email=from_email, to=[to_email])
    email.send()
