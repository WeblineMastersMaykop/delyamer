import requests
import json
from datetime import date
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from core.tokens import account_activation_token, change_email_token
from core.models import MailFromString, MailToString
from core.templatetags.tags import only_digits


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


def order_pay_response(request, order):
    data = {
        'userName': 'delyamer-api',
        'password': 'delyamer',
        'orderNumber': order.id,
        'returnUrl': 'http://{}{}{}/'.format(get_current_site(request).domain, '/orders/done/', order.id),
        'failUrl': 'http://{}{}{}/'.format(get_current_site(request).domain, '/orders/fail/', order.id),
        'amount': order.total_price_with_sale * 100
    }

    r = requests.post('https://3dsec.sberbank.ru/payment/rest/register.do', data=data)
    r_text = json.loads(r.text)

    return r_text.get('formUrl')


def order_pay_credit(request, order):
    items = [
        {
            "positionId": pos,
            "name": item.offer.product.name,
            "quantity": {
                "value": item.quantity,
                "measure": "шт."
            },
            "itemAmount": item.total_price_with_sale * 100,
            "itemPrice": item.total_price_with_sale // item.quantity * 100,
            "itemCode": item.offer.id,
        }
        for pos, item in enumerate(order.items.all(), 1)
    ]

    items.append({
        "positionId": len(items) + 2,
        "name": "Доставка",
        "quantity": {
            "value": 1,
            "measure": "шт."
        },
        "itemAmount": order.delivery_price * 100,
        "itemPrice": order.delivery_price * 100,
        "itemCode": 0,
    })

    data = {
        "dummy": False,
        "userName": "delyamer-credit-api",
        "password": "delyamer-credit",
        "orderNumber": order.id,
        "currency": 643,
        "returnUrl": "http://{}{}{}/".format(get_current_site(request).domain, "/orders/done/", order.id),
        "failUrl": "http://{}{}{}/".format(get_current_site(request).domain, "/orders/fail/", order.id),
        "amount": order.total_price_with_sale * 100,
        "jsonParams": {
            "email": order.email,
            "phone": only_digits(order.phone),
            "backToShopUrl": "http://{}/orders/cart/".format(get_current_site(request).domain)
        },
        "orderBundle": {
            # "orderCreationDate": order.created.strftime("%Y:%m:%dT%H:%M:%S"),
            "cartItems": {
                "items": items,
            },
            "installments": {
                "productType": "INSTALLMENT",
                "productID": "10"
            }
        }
    }

    payload_str = "&".join("{}={}".format(key, val) for key, val in data.items())
    payload_str = payload_str.replace("'", '"')

    r = requests.post("https://3dsec.sberbank.ru/sbercredit/register.do?{}".format(payload_str))
    r_text = json.loads(r.text)

    return r_text.get('formUrl')


def calc_cdeck_delivery(receiver_postcode):
    data = {
        'version': '1.0',
        'dateExecute': date.today().strftime('%Y-%m-%d'),
        'authLogin': 'fPFWQzTQvGqRPLRkSIU2HOqFd7MnRPMZ',
        'secure': 'bgnQbfsRPJaUAGraihgtbc6j07PJJO60',
        'senderCityPostCode': '350000',
        'receiverCityPostCode': receiver_postcode,
        'tariffId': 137,
        # 'tariffList': [
        #     {'id': 136},
        #     {'id': 137},
        #     {'id': 139},
        #     {'id': 233},
        #     {'id': 234},
        # ],
        'goods': [
            {
                'weight': '0.5',
                'length': '30',
                'width': '20',
                'height': '10'
            }
        ]
    }

    r = requests.post('http://api.cdek.ru/calculator/calculate_price_by_json.php', json=data)
    r_text = json.loads(r.text)

    result = None
    try:
        result = r_text['result']['price']
    except Exception as e:
        print(e)

    return result


def get_insta_posts():
    from instagram_web_api import Client, ClientCompatPatch

    user_name = 'gurgen_xd'
    password = 'WORDpassim1995'

    api = Client()
    user_feed_info = web_api.user_feed('329452045', count=10)
    for post in user_feed_info:
        print('%s from %s' % (post['link'], post['user']['username']))
    # results = api.feed_timeline()
    # items = results.get('items', [])
    # for item in items:
    #     # Manually patch the entity to match the public api as closely as possible, optional
    #     # To automatically patch entities, initialise the Client with auto_patch=True
    #     ClientCompatPatch.media(item)
    #     print(media['code'])