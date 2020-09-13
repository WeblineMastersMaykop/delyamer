import math
from products.models import Offer, FavoriteProduct
from promotions.models import PromotionSumPresent, PromotionThreeSales, PromotionMinPresent, PromotionSale
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
        # self.cart[str(offer.id)]['cost'] = offer.get_price() * quantity
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
            # self.cart[offer_id]['price_with_sale'] = offer_price
            # self.cart[offer_id]['cost'] = self.get_cost(offer)
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
        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())

    def get_sale(self):
        pr_sales = PromotionSale.objects.all()
        result = 0

        for pr in pr_sales:
            for item in self.cart.values():
                if int(item['promotion_sale']) == pr.id:
                    result += math.ceil(self.get_cost(str(item['offer_id'])) * pr.sale / 100)
        return result

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
        return result

    def get_total_price_with_sales(self):
        return 2510


    def get_cost(self, offer_id):
        offer_info = self.cart[offer_id]
        return int(offer_info['price']) * int(offer_info['quantity'])

    # def get_cost_with_sale(self, offer_id):
    #     offer_info = self.cart[offer_id]
    #     return int(offer_info['price_with_sale']) * int(offer_info['quantity'])

    def clear(self):
        del self.session['cart']
        self.session.modified = True