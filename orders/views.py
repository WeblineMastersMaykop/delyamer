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

        context = {
            'price': delivery.price,
        }
        return JsonResponse(context)


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

        cart.add(offer)

        context = {
            'cart_len': len(cart),
        }
        return JsonResponse(context)


class RemoveFromCartView(View):
    def get(self, request):
        cart = Cart(request)

        offer_id = request.GET.get('offer')
        offer = get_object_or_404(Offer, pk=offer_id)
        cart.remove(offer)

        context = {
            'cart_len': len(cart),
        }
        return JsonResponse(context)


class ChangeQuantityView(View):
    def get(self, request):
        cart = Cart(request)

        offer_id = request.GET.get('offer')
        quantity = request.GET.get('quantity', 1)

        offer = get_object_or_404(Offer, pk=offer_id)
        cart.change_quantity(offer, int(quantity))

        context = {
            'cart_len': len(cart),
            'cost': cart.get_cost(offer_id),
            'total_price': cart.get_total_price()
        }
        return JsonResponse(context)


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

            order = Order.objects.create(
                user=user if user.is_authenticated else None,
                full_name=full_name,
                phone=phone
            )

            OrderItem.objects.create(
                order=order,
                offer=offer,
                price=offer.get_price(),
                quantity=1
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
            order = order_form.save(commit=False)
            order.user = user if user.is_authenticated else None
            order.save()

            for item in cart:
                offer = Offer.objects.get(pk=item['offer_id'])
                offer.stock -= int(item['quantity'])
                offer.save()

                OrderItem.objects.create(
                    order=order,
                    offer=offer,
                    price=offer.get_price(),
                    quantity=item['quantity']
                )

            form_url = order_pay_response(request, order, cart.get_total_price_with_sales())
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
        cart = Cart(request)
        cart.clear()

        send_order_mail(request, order)

        context = {
            'order': order
        }
        return render(request, 'orders/order-done.html', context)


class OrderFailView(View):
    def get(self, request):

        context = {
        }
        return render(request, 'orders/order-fail.html', context)
