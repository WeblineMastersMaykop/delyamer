import requests
import json
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from core.tokens import account_activation_token, change_email_token
from core.models import MailFromString, MailToString


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


def send_order_mail(request, order):
    current_site = get_current_site(request)
    subject = 'Новый заказ на сайте'

    template = 'orders/order-message.html'

    message = render_to_string(template, {
        'domain': current_site.domain,
        'order': order,
    })

    from_email = MailFromString.objects.first().host_user
    to_email = [item.email for item in MailToString.objects.all()]
    email = EmailMessage(subject, message, from_email=from_email, to=to_email)
    email.send()


def order_pay_response(request, order, total_price):
    auth_data = {
        'userName': 'delyamer-api',
        'password': 'delyamer',
        'orderNumber': order.id,
        'returnUrl': 'http://{}{}{}/'.format(get_current_site(request).domain, '/orders/done/', order.id),
        'failUrl': 'http://{}{}{}/'.format(get_current_site(request).domain, '/orders/fail/', order.id),
        'amount': total_price * 100
    }

    r = requests.post('https://3dsec.sberbank.ru/payment/rest/register.do', data=auth_data)
    r_text = json.loads(r.text)

    return r_text.get('formUrl')
