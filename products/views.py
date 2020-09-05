from django.shortcuts import render, get_object_or_404
from django.views import View
from products.models import Category, Product, Offer
from pages.models import Page
from django.db.models import F
from django.db.models.functions import Coalesce
from core.paginator import pagination


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
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        color_list = request.GET.getlist('color')
        size_list = request.GET.getlist('size')
        pushup = request.GET.getlist('pushup')

        get_request = request.GET.copy()

        category = Category.objects.none()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            offers = Offer.objects.filter(
                product__category=category, product__is_active=True, is_active=True).select_related(
                'product', 'promotion_sale').annotate(
                price_with_sale=F('product__price') * (100 - Coalesce(F('promotion_sale__sale'), 0)) / 100)
        else:
            offers = Offer.objects.filter(product__is_active=True, is_active=True).select_related(
                'product', 'promotion_sale').annotate(
                price_with_sale=F('product__price') * (100 - Coalesce(F('promotion_sale__sale'), 0)) / 100)

        try:
            is_new = int(is_new)
            offers = offers.filter(product__is_new=is_new)
        except:
            get_request.pop('is_new', None)

        if pushup:
            try:
                pushup = map(int, pushup)
                offers = offers.filter(product__pushup__in=pushup)
            except:
                get_request.pop('pushup', None)

        if color_list:
            try:
                color_list = map(int, color_list)
                offers = offers.filter(color__in=color_list)
            except:
                get_request.pop('color_list', None)

        if size_list:
            try:
                size_list = map(int, size_list)
                offers = offers.filter(size__in=size_list)
            except:
                get_request.pop('size_list', None)

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

        offers = offers.order_by('product__id', '-price_with_sale')

        main_offers = []
        offer_old = None
        for offer in offers:
            if offer.product.id != offer_old:
                main_offers.append(offer)
                offer_old = offer.product.id

        page_number = request.GET.get('page', 1)
        pag_res = pagination(main_offers, page_number, get_request)

        context = {
            'category': category,
            'main_offers': main_offers,
            'page_object': pag_res['page'],
            'is_paginated': pag_res['is_paginated'],
            'next_url': pag_res['next_url'],
            'prev_url': pag_res['prev_url'],
        }
        return render(request, 'products/products.html', context)


class ProductView(View):
    def get(self, request, category_slug, product_slug):
        print(category_slug, product_slug)
        product = get_object_or_404(Product, slug=product_slug)

        try:
            parents = Page.objects.get(action='products').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        context = {
            'product': product,
            'parents': parents,
        }
        return render(request, 'products/product.html', context)
