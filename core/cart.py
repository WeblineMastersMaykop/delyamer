import math
from products.models import Offer, FavoriteProduct
from promotions.models import PromotionSumPresent, PromotionThreeSales, PromotionMinPresent, PromotionSale, PromoCode
from orders.models import DeliveryMethod


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

        delivery = self.session.get('delivery')
        if not delivery:
            delivery_method = DeliveryMethod.objects.first()
            delivery = self.session['delivery'] = (delivery_method.id, delivery_method.price)
        self.delivery = delivery

        promocode = PromoCode.objects.filter(code=self.session.get('promocode'))
        if promocode.exists():
            self.promocode = promocode.first()
        else:
            self.promocode = self.session['promocode'] = None

    def change_delivery(self, delivery_method):
        self.delivery = (delivery_method.id, delivery_method.price)
        self.session['delivery'] = self.delivery
        self.session.modified = True

    def add(self, offer):
        self.cart[str(offer.id)] = {
            'quantity': 1,
            'offer_id': offer.id,
        }
        self.save()

    def change_quantity(self, offer, quantity):
        self.cart[str(offer.id)]['quantity'] = quantity
        self.save()

    def remove(self, offer):
        offer_id = str(offer.id)
        if offer_id in self.cart:
            del self.cart[offer_id]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        offer_ids = self.cart.keys()
        offers = Offer.objects.filter(id__in=offer_ids)

        for offer in offers:
            offer_price = offer.get_price()
            offer_id = str(offer.id)
            self.cart[offer_id]['price'] = offer.product.price
            self.cart[offer_id]['name'] = offer.product.name
            self.cart[offer_id]['color'] = offer.color.name if offer.color else None
            self.cart[offer_id]['size'] = offer.size.name if offer.size else None
            self.cart[offer_id]['cup'] = offer.cup.name if offer.cup else None
            self.cart[offer_id]['url'] = offer.product.get_absolute_url()
            self.cart[offer_id]['stock'] = offer.stock
            self.cart[offer_id]['image_url'] = offer.get_image().image_small.url
            self.cart[offer_id]['promotion_sale'] = offer.promotion_sale.id if offer.promotion_sale else -1
            self.cart[offer_id]['promotion_sum_present'] = offer.promotion_sum_present.id if offer.promotion_sum_present else -1
            self.cart[offer_id]['promotion_three_sales'] = offer.promotion_three_sales.id if offer.promotion_three_sales else -1
            self.cart[offer_id]['promotion_min_present'] = offer.promotion_min_present.id if offer.promotion_min_present else -1
            self.session.modified = True
            yield self.cart[offer_id]

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        self.total_price = sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())
        return self.total_price

    def get_sale(self):
        pr_sales = PromotionSale.objects.all()
        result = 0

        for pr in pr_sales:
            for item in self.cart.values():
                if int(item['promotion_sale']) == pr.id:
                    result += math.ceil(self.get_cost(str(item['offer_id'])) * pr.sale / 100)
        self.promotion_sale = result
        return self.promotion_sale

    def get_three_sales(self):
        pr_three_sales = PromotionThreeSales.objects.all()
        total_price = self.get_total_price()
        result = 0

        for pr in pr_three_sales:
            if total_price >= pr.price3:
                for item in self.cart.values():
                    if int(item['promotion_three_sales']) == pr.id:
                        result += math.ceil(self.get_cost(str(item['offer_id'])) * pr.sale3 / 100)
            elif total_price >= pr.price2:
                for item in self.cart.values():
                    if int(item['promotion_three_sales']) == pr.id:
                        result += math.ceil(self.get_cost(str(item['offer_id'])) * pr.sale2 / 100)
            elif total_price >= pr.price1:
                for item in self.cart.values():
                    if int(item['promotion_three_sales']) == pr.id:
                        result += math.ceil(self.get_cost(str(item['offer_id'])) * pr.sale1 / 100)
        self.promotion_three_sales = result
        return self.promotion_three_sales

    def get_sum_present(self):
        pr_sum_present = PromotionSumPresent.objects.all()
        total_price = self.get_total_price()
        values = set()

        for pr in pr_sum_present:
            if total_price >= pr.total_price:
                for item in self.cart.values():
                    offer_price = int(item['price'])
                    if int(item['promotion_sum_present']) == pr.id and offer_price <= pr.price:
                        values.add(offer_price)

        result = min(values) if values else 0
        self.promotion_sum_present = result
        return self.promotion_sum_present

    def get_min_present(self):
        pr_min_present = PromotionMinPresent.objects.all()
        values = set()
        cart_len = sum(int(item['quantity']) for item in self.cart.values())

        for pr in pr_min_present:
            if cart_len >= pr.nmb:
                for item in self.cart.values():
                    if int(item['promotion_min_present']) == pr.id:
                        values.add(int(item['price']))

        result = min(values) if values else 0
        self.promotion_min_present = result
        return self.promotion_min_present

    def update_sales(self):
        self.get_sale()
        self.get_sum_present()
        self.get_three_sales()
        self.get_min_present()
        self.get_total_sale()

    def get_total_sale(self):
        self.total_sale = self.promotion_sale + self.promotion_sum_present \
                          + self.promotion_three_sales + self.promotion_min_present
        return self.total_sale

    def get_total_price_with_sales(self):
        result = self.total_price - self.total_sale
        if self.promocode:
            result = math.ceil(result * (100 - self.promocode.sale ) / 100)
        result += self.delivery[1]
        return result

    def get_promocode_price(self):
        self.get_total_sale()
        total_price = self.total_price - self.total_sale
        result = 0

        if self.promocode:
            result = self.promocode.sale * total_price // 100
        return result

    def get_cost(self, offer_id):
        offer_info = self.cart[offer_id]
        return int(offer_info['price']) * int(offer_info['quantity'])

    def set_promocode(self, code):
        promocode = PromoCode.objects.filter(code=code)
        if promocode.exists():
            self.promocode = promocode.first()
            self.session['promocode'] = self.promocode.code
        else:
            self.promocode = self.session['promocode'] = None
        self.session.modified = True
        return self.promocode

    def clear(self):
        del self.session['cart']
        del self.session['promocode']
        del self.session['delivery']
        self.session.modified = True