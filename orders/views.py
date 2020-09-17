from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from core.utils import send_order_mail, order_pay_response
from core.models import MailToString
from products.models import Offer, Product
from orders.models import Order, OrderItem, DeliveryMethod
from orders.forms import OrderForm
from core.cart import Cart


class CartView(View):
    def get(self, request):
        delivery_methods = DeliveryMethod.objects.all()
        user = request.user
        order_form = OrderForm(instance=user if user.is_authenticated else None)

        context = {
            'delivery_methods': delivery_methods,
            'order_form': order_form,
        }
        return render(request, 'orders/cart.html', context)


class ChangeDeliveryView(View):
    def get(self, request):
        cart = Cart(request)

        delivery_id = request.GET.get('delivery')
        delivery = get_object_or_404(DeliveryMethod, pk=delivery_id)
        cart.change_delivery(delivery)
        return redirect('cart')


class AddToCartView(View):
    def get(self, request):
        cart = Cart(request)

        product_id = request.GET.get('product')
        color_id = request.GET.get('color') or None
        size_id = request.GET.get('size') or None
        cup_id = request.GET.get('cup') or None

        offer = get_object_or_404(
            Offer.objects.select_related('color', 'size', 'cup'),
            product__id=product_id, is_active=True, color=color_id, size=size_id, cup=cup_id
        )
        cart.add(offer.id)
        return redirect(request.META.get('HTTP_REFERER'))


class RemoveFromCartView(View):
    def get(self, request):
        cart = Cart(request)

        offer_id = request.GET.get('offer_id')
        offer = get_object_or_404(Offer, pk=offer_id)
        cart.remove(offer.id)
        return redirect('cart')


class ChangeQuantityView(View):
    def get(self, request):
        cart = Cart(request)

        offer_id = request.GET.get('offer_id')
        quantity = request.GET.get('quantity', 1)

        offer = get_object_or_404(Offer, pk=offer_id)
        cart.change_quantity(offer.id, int(quantity))
        return redirect('cart')


class AddPromocodeView(View):
    def get(self, request):
        code = request.GET.get('promocode')
        cart = Cart(request)
        promocode = cart.set_promocode(code)
        return redirect('cart')


class RemovePromocodeView(View):
    def get(self, request):
        cart = Cart(request)
        promocode = cart.set_promocode(None)
        return redirect('cart')


class OrderOneClickAddView(View):
    def post(self, request):
        product_id = request.POST.get('product')
        color_id = request.POST.get('color')
        size_id = request.POST.get('size')
        cup_id = request.POST.get('cup')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')

        try:
            offer = Offer.objects.get(product__id=product_id, color__id=color_id, size__id=size_id, cup__id=cup_id)
            user = request.user
            offer_price = offer.product.price
            offer_price_with_sale = offer.get_price()

            order = Order.objects.create(
                user=user if user.is_authenticated else None,
                full_name=full_name,
                phone=phone,
                total_price=offer_price,
                total_price_with_sale=offer_price_with_sale,
            )

            OrderItem.objects.create(
                order=order,
                offer=offer,
                price=offer_price,
                total_price_with_sale=offer_price_with_sale,
                discount=offer_price-offer_price_with_sale,
            )

            offer.stock -= 1
            offer.save()

            send_order_mail(request, order)
            success = True
        except Exception as e:
            print(e)
            success = False

        context = {
            'success': success,
        }
        return JsonResponse(context)


class OrderAddView(View):
    def post(self, request):
        order_form = OrderForm(request.POST)

        cart = Cart(request)
        user = request.user

        if order_form.is_valid():
            order = order_form.save()
            order_items = []

            for item in cart:
                offer = item['offer']

                if item['has_present']:
                    order_item = OrderItem(
                        order=order,
                        offer=offer,
                        price=item['price'],
                        discount=item['price'],
                        total_price_with_sale=0,
                        quantity=1
                    )
                    order_items.append(order_item)

                    if item['quantity'] - 1:
                        order_item = OrderItem(
                            order=order,
                            offer=offer,
                            price=item['price'],
                            discount=item['cost']-item['cost_with_sale']-item['price'],
                            total_price_with_sale=item['cost_with_sale'],
                            quantity=item['quantity']-1
                        )
                        order_items.append(order_item)
                else:
                    order_item = OrderItem(
                        order=order,
                        offer=offer,
                        price=item['price'],
                        discount=item['cost']-item['cost_with_sale'],
                        total_price_with_sale=item['cost_with_sale'],
                        quantity=item['quantity']
                    )
                    order_items.append(order_item)

                offer.stock -= int(item['quantity'])

            order.total_price = cart.offers_price + cart.delivery[1]
            order.total_price_with_sale = cart.get_total_price()
            order.user = user if user.is_authenticated else None
            order.save()

            OrderItem.objects.bulk_create(order_items)

            Offer.objects.bulk_update(cart.offers, ['stock'])

            form_url = order_pay_response(request, order)
            return redirect(form_url)

        delivery_methods = DeliveryMethod.objects.all()

        context = {
            'delivery_methods': delivery_methods,
            'order_form': order_form,
        }
        return render(request, 'orders/cart.html', context)


class OrderDoneView(View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        order.status = 'paid'
        order.save()

        cart = Cart(request)
        cart.clear()

        send_order_mail(request, order)

        context = {
            'order': order
        }
        return render(request, 'orders/order-done.html', context)


class OrderFailView(View):
    def get(self, request, order_id):

        context = {
        }
        return render(request, 'orders/order-fail.html', context)
