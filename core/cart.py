from django.forms.models import model_to_dict
from products.models import Offer


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, offer, quantity):
        offer_id = str(offer.id)
        if offer_id not in self.cart:
            self.cart[offer_id] = {
                'quantity': quantity,
                'price': offer.product.price,
                'cost': offer.product.price * quantity,
                'offer_name': offer.product.name,
                'offer_color': offer.color.name,
                'offer_size': offer.size.name,
                'offer_url': offer.product.get_absolute_url(),
                'offer_id': offer.id,
                #'offer_stock': offer.stock,
                # 'offer_image_url': offer.product.get_main_image().image.url
            }
        else:
            self.cart[offer_id]['quantity'] = int(self.cart[offer_id]['quantity']) + quantity
            self.cart[offer_id]['cost'] = int(self.cart[offer_id]['cost']) + offer.product.price * quantity
        self.save()

    def change_quantity(self, offer, quantity):
        self.cart[str(offer.id)]['quantity'] = quantity
        self.cart[str(offer.id)]['cost'] = offer.product.price * quantity
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
        # offer_ids = self.cart.keys()
        # offers = Offer.objects.filter(id__in=offer_ids)

        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['quantity'] = int(item['quantity'])
            item['cost'] = int(item['cost'])
            yield item
    
    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.session.modified = True