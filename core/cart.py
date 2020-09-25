from products.models import Offer
from promotions.models import PromotionSumPresent, PromotionThreeSales, PromotionMinPresent, PromotionSale, PromoCode


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

        delivery = self.session.get('delivery')
        if not delivery:
            delivery = self.session['delivery'] = {
                'method': None,
                'price': 0,
                'postcode': None
            }
        self.delivery = delivery

        promocode = PromoCode.objects.filter(code=self.session.get('promocode'))
        if promocode.exists():
            self.promocode = promocode.first()
        else:
            self.promocode = self.session['promocode'] = None

        self.sum_sale = 0
        self.sum_three_sales = 0
        self.sum_sum_present = 0
        self.sum_min_present = 0
        self.sum_promocode = 0

    def __len__(self):
        return sum(int(item) for item in self.cart.values())

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        del self.session['promocode']
        del self.session['delivery']
        self.session.modified = True

    def add(self, offer_id):
        offer_id = str(offer_id)
        self.cart[offer_id] = '1'
        self.save()

    def change_quantity(self, offer_id, quantity):
        offer_id = str(offer_id)
        if self.cart.get(offer_id):
            self.cart[offer_id] = str(quantity)
            self.save()

    def remove(self, offer_id):
        offer_id = str(offer_id)
        self.cart.pop(offer_id, None)
        self.save()

    def __iter__(self):
        self.sales = PromotionSale.objects.all()
        self.three_sales = PromotionThreeSales.objects.all()
        self.min_present_sales = PromotionMinPresent.objects.all()
        self.sum_present_sales = PromotionSumPresent.objects.all()
        self.promocodes = PromoCode.objects.all()
        self.min_present = True
        self.sum_present = True

        for offer in self.offers:
            price = offer.product.price
            price_with_sale, has_present, sum_sale, sum_sum_present, sum_three_sales, sum_min_present, sum_promocode = self.offer_price(offer)
            quantity = int(self.cart[str(offer.id)])
            cost = price * quantity
            cost_with_sale = price_with_sale * quantity - has_present * price_with_sale

            self.sum_sale += sum_sale * quantity
            self.sum_three_sales += sum_three_sales * quantity
            self.sum_sum_present += sum_sum_present
            self.sum_min_present += sum_min_present
            self.sum_promocode += sum_promocode * quantity

            offer_promo = offer.promotion_three_sales or offer.promotion_sale or offer.promotion_sum_present or offer.promotion_min_present
            offer_promo_text = offer_promo.text if offer_promo else None

            item = {
                'offer_promo_text': offer_promo_text,
                'offer': offer,
                'id': offer.id,
                'quantity': quantity,
                'price': price,
                'price_with_sale': price_with_sale,
                'cost': cost,
                'cost_with_sale': cost_with_sale,
                'has_present': has_present,
                'name': offer.product.name,
                'color': offer.color.name if offer.color else None,
                'size': offer.size.name if offer.size else None,
                'cup': offer.cup.name if offer.cup else None,
                'url': offer.product.get_absolute_url(),
                'stock': offer.stock,
                'image_url': offer.get_image().image_small.url,
            }
            yield item

    @property
    def offers_price(self):
        result = 0
        if self.offers:
            result = sum(offer.product.price * int(self.cart[str(offer.id)]) for offer in self.offers)
        return result

    @property
    def offers(self):
        offer_ids = self.cart.keys()
        return Offer.objects.filter(id__in=offer_ids, is_active=True, stock__gt=0).select_related(
            'product', 'size', 'color', 'cup', 'promotion_sum_present',
            'promotion_three_sales', 'promotion_min_present', 'promotion_sale'
        ).order_by('product__price')

    def get_total_sale(self):
        return self.sum_sale + self.sum_three_sales \
               + self.sum_sum_present + self.sum_min_present + self.sum_promocode

    def get_total_price(self):
        return self.offers_price + int(self.delivery['price']) - self.get_total_sale()

    def offer_price(self, offer):
        price = offer.product.price
        has_present = False
        sum_sale = 0
        sum_three_sales = 0
        sum_sum_present = 0
        sum_min_present = 0
        sum_promocode = 0

        if offer.promotion_sale:
            sum_sale = offer.product.price * offer.promotion_sale.sale // 100
            price =  offer.product.price - sum_sale
        elif offer.promotion_three_sales:
            sale = 0
            if self.offers_price >= offer.promotion_three_sales.price3:
                sale = offer.promotion_three_sales.sale3
            elif self.offers_price >= offer.promotion_three_sales.price2:
                sale = offer.promotion_three_sales.sale2
            elif self.offers_price >= offer.promotion_three_sales.price1:
                sale = offer.promotion_three_sales.sale1
            sum_three_sales = offer.product.price * sale // 100
            price = offer.product.price - sum_three_sales
        elif offer.promotion_min_present:
            if (len(self.cart) >= offer.promotion_min_present.nmb and
                self.min_present):
                sum_min_present = price
                has_present = True
                self.min_present = False
        elif offer.promotion_sum_present:
            if (self.offers_price >= offer.promotion_sum_present.total_price and
                price <= offer.promotion_sum_present.price and self.sum_present):
                    sum_sum_present = price
                    has_present = True
                    self.sum_present = False

        if self.promocode:
            sum_promocode = price * self.promocode.sale // 100
            price = price - sum_promocode

        return price, has_present, sum_sale, sum_sum_present, sum_three_sales, sum_min_present, sum_promocode

    def set_promocode(self, code):
        promocode = PromoCode.objects.filter(code=code)
        if promocode.exists():
            self.promocode = promocode.first()
            self.session['promocode'] = self.promocode.code
        else:
            self.promocode = self.session['promocode'] = None
        self.session.modified = True
        return self.promocode

    def change_delivery(self, method, price, postcode):
        self.delivery = {
            'method': method,
            'price': price,
            'postcode': postcode
        }
        self.session['delivery'] = self.delivery
        self.session.modified = True
