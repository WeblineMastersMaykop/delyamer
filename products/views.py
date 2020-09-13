from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.db.models import F, Case, When, Value, BooleanField
from django.db.models.functions import Coalesce
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Category, Product, Offer, Color, Size, Cup, FavoriteProduct
from pages.models import Page
from orders.models import Review
from orders.forms import OrderOneClickForm
from core.paginator import pagination
from core.cart import Cart


class CategoriesView(View):
    def get(self, request):
        try:
            parents = Page.objects.get(action='products').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        context = {
            'parents': parents,
        }
        return render(request, 'products/categories.html', context)


class ProductsView(View):
    def get(self, request):
        category_slug = request.GET.get('category')
        is_new = request.GET.get('is_new')
        in_sale = request.GET.get('in_sale')
        is_bs = request.GET.get('is_bs')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        color_list = request.GET.getlist('color', [])
        size_list = request.GET.getlist('size', [])
        cup_list = request.GET.getlist('cup', [])
        pushup = request.GET.get('pushup')
        ordering = request.GET.get('ordering', 1)

        get_request = request.GET.copy()

        category = Category.objects.none()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            offers = Offer.objects.filter(
                product__category=category, product__is_active=True, is_active=True).select_related(
                'product', 'promotion_sale', 'color', 'size', 'cup').annotate(
                price_with_sale=F('product__price') * (100 - Coalesce(F('promotion_sale__sale'), 0)) / 100)
        else:
            offers = Offer.objects.filter(product__is_active=True, is_active=True).select_related(
                'product', 'promotion_sale', 'color', 'size', 'cup').annotate(
                price_with_sale=F('product__price') * (100 - Coalesce(F('promotion_sale__sale'), 0)) / 100)

        try:
            is_bs = int(is_bs)
            offers = offers.filter(product__is_bs=is_bs)
        except:
            get_request.pop('is_bs', None)

        try:
            is_new = int(is_new)
            offers = offers.filter(product__is_new=is_new)
        except:
            get_request.pop('is_new', None)

        try:
            pushup = int(pushup)
            offers = offers.filter(product__pushup=pushup)
        except:
            get_request.pop('pushup', None)

        if color_list:
            try:
                color_list = list(map(int, color_list))
                offers = offers.filter(color__in=color_list)
            except:
                get_request.pop('color_list', None)

        if size_list:
            try:
                size_list = list(map(int, size_list))
                offers = offers.filter(size__in=size_list)
            except:
                get_request.pop('size_list', None)

        if cup_list:
            try:
                cup_list = list(map(int, cup_list))
                offers = offers.filter(cup__in=cup_list)
            except:
                get_request.pop('cup_list', None)

        try:
            price_min = int(price_min)
            offers = offers.filter(price_with_sale__gte=price_min)
        except:
            get_request.pop('price_min', None)

        try:
            price_max = int(price_max)
            offers = offers.filter(price_with_sale__lte=price_max)
        except:
            get_request.pop('price_max', None)

        try:
            in_sale = int(in_sale)
            offers = offers.exclude(promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=None, promotion_sale=None)
        except:
            get_request.pop('in_sale', None)

        offers = offers.order_by('product__id', 'price_with_sale')

        main_offers = []
        offer_old = None
        for offer in offers:
            if offer.product.id != offer_old:
                main_offers.append(offer)
                offer_old = offer.product.id

        if ordering:
            try:
                ordering = int(ordering)
                if ordering == 1:
                    main_offers.sort(key=lambda offer: offer.product.is_bs, reverse=True)
                elif ordering == 2:
                    main_offers.sort(key=lambda offer: offer.price_with_sale)
                elif ordering == 3:
                    main_offers.sort(key=lambda offer: offer.price_with_sale, reverse=True)
                elif ordering == 4:
                    main_offers.sort(key=lambda offer: offer.product.is_new, reverse=True)
                elif ordering == 5:
                    main_offers.sort(key=lambda offer: offer.promotion_sale if offer.promotion_sale else 0, reverse=True)
            except:
                get_request.pop('ordering', None)

        page_number = request.GET.get('page', 1)
        pag_res = pagination(main_offers, page_number, get_request)

        colors = Color.objects.all().annotate(checked=Case(
            When(id__in=color_list, then=Value(1)),
            default=0,
            output_field=BooleanField()
        ))

        sizes = Size.objects.all().annotate(checked=Case(
            When(id__in=size_list, then=Value(1)),
            default=0,
            output_field=BooleanField()
        ))

        cups = Cup.objects.all().annotate(checked=Case(
            When(id__in=cup_list, then=Value(1)),
            default=0,
            output_field=BooleanField()
        ))

        if category:
            category_name = category.name
        elif in_sale:
            category_name = 'Распродажа'
        elif is_new:
            category_name = 'Новинки'
        else:
            category_name = 'Все товары'

        context = {
            'price_min': price_min or '',
            'price_max': price_max or '',
            'ordering': ordering,
            'category_slug': category_slug,
            'category_name': category_name,

            'colors': colors,
            'sizes': sizes,
            'cups': cups,
            'pushup': pushup,
            'category': category,
            'main_offers': main_offers,

            'page_object': pag_res['page'],
            'is_paginated': pag_res['is_paginated'],
            'next_url': pag_res['next_url'],
            'prev_url': pag_res['prev_url'],
        }
        return render(request, 'products/products.html', context)


class ProductView(View):
    def get(self, request, product_slug):
        product = get_object_or_404(Product.objects.select_related('category'), slug=product_slug, is_active=True)
        main_offer = product.main_offer()

        color_id = main_offer.color.id if main_offer.color else None
        size_id = main_offer.size.id if main_offer.size else None
        cup_id = main_offer.cup.id if main_offer.cup else None

        sizes = product.get_sizes(color_id=color_id, cup_id=cup_id)
        colors = product.get_colors(size_id=size_id, cup_id=cup_id)
        cups = product.get_cups(color_id=color_id, size_id=size_id)

        reviews = Review.objects.select_related('order_item', 'order_item__offer', 'order_item__offer__product' ).filter(order_item__offer__product__id=product.id)

        try:
            rating = round(sum(int(review.get_rating_display()) for review in reviews) / reviews.count())
        except:
            rating = 0

        page_number = request.GET.get('page', 1)
        pag_res = pagination(reviews, page_number, request.GET.copy())

        order_ocf = OrderOneClickForm()

        context = {
            'order_ocf': order_ocf,
            'colors': colors,
            'cups': cups,
            'sizes': sizes,
            'product': product,
            'main_offer': main_offer,
            'reviews': reviews,
            'rating': str(rating),

            'page_object': pag_res['page'],
            'is_paginated': pag_res['is_paginated'],
            'next_url': pag_res['next_url'],
            'prev_url': pag_res['prev_url'],
        }
        return render(request, 'products/product.html', context)


class ChangeOfferView(View):
    def get(self, request):
        product_id = request.GET.get('product')
        color_id = request.GET.get('color')
        size_id = request.GET.get('size')
        cup_id = request.GET.get('cup')
        btn_type = request.GET.get('btn_type')

        print(color_id, size_id, cup_id)

        product = Product.objects.get(pk=product_id)
        sizes, colors, cups = [], [], []

        offer = Offer.objects.filter(product__id=product_id, color__id=color_id, size__id=size_id, cup__id=cup_id).first()

        if btn_type == 'color':
            if not offer:
                offer = Offer.objects.filter(product__id=product_id, color__id=color_id).first()
            for size in product.get_sizes(color_id=color_id, cup_id=cup_id):
                checked = 1 if offer.size == size else 0
                sizes.append((size.id, size.name, checked))
            for cup in product.get_cups(color_id=color_id, size_id=size_id):
                checked = 1 if offer.cup == cup else 0
                cups.append((cup.id, cup.name, checked))
        elif btn_type == 'size':
            if not offer:
                offer = Offer.objects.filter(product__id=product_id, size__id=size_id).first()
            for color in product.get_colors(size_id=size_id, cup_id=cup_id):
                checked = 1 if offer.color == color else 0
                colors.append((color.id, color.color, checked))
            for cup in product.get_cups(color_id=color_id, size_id=size_id):
                checked = 1 if offer.cup == cup else 0
                cups.append((cup.id, cup.name, checked))
        elif btn_type == 'cup':
            if not offer:
                offer = Offer.objects.filter(product__id=product_id, cup__id=cup_id).first()
            for color in product.get_colors(size_id=size_id, cup_id=cup_id):
                checked = 1 if offer.color == color else 0
                colors.append((color.id, color.color, checked))
            for size in product.get_sizes(color_id=color_id, cup_id=cup_id):
                checked = 1 if offer.size == size else 0
                sizes.append((size.id, size.name, checked))

        image_id = offer.get_image().id

        cart = Cart(request)
        in_cart = 1 if str(offer.id) in cart.cart else 0

        print(cups)
        print(colors)
        print(sizes)

        context = {
            'success': True,
            'btn_type': btn_type,
            'sizes': sizes,
            'colors': colors,
            'cups': cups,
            'product_price': offer.product.price,
            'offer_price': offer.get_price(),
            'offer_stock': 'Много' if offer.stock > 10 else 'Мало',
            'image_id': image_id,
            'in_cart': in_cart,
        }
        return JsonResponse(context)


class FavoriteProductsView(View):
    def get(self, request):
        favorites = FavoriteProduct.objects.filter(user=request.user).select_related('offer', 'offer__product')

        context = {
            'favorites': favorites,
        }
        return render(request, 'products/favorite.html', context)


class RemoveFavoriteView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        favorite_id = request.GET.get('favorite')
        favorite = get_object_or_404(FavoriteProduct, pk=favorite_id, user=request.user)
        favorite.delete()

        return JsonResponse({})


class AddFavoriteView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        offer_id = request.GET.get('offer')
        offer = get_object_or_404(Offer, pk=offer_id)
        favorite = FavoriteProduct.objects.create(
            offer=offer,
            user=request.user
        )

        return JsonResponse({})
