from django.shortcuts import render
from django.views import View
from news.models import News
from products.models import Product
from core.models import Slide, InstagramPhotos


class IndexView(View):
    def get(self, request):
        index_news = News.objects.filter(is_active=True)[:3]
        bs_products = Product.objects.filter(is_active=True, is_bs=True)[:8]
        new_products = Product.objects.filter(is_active=True, is_new=True)[:8]
        slides = Slide.objects.all()
        insta_photos = InstagramPhotos.objects.all()[:8]

        context = {
            'insta_photos': insta_photos,
            'index_news': index_news,
            'bs_products': bs_products,
            'new_products': new_products,
            'slides': slides,
        }
        return render(request, 'core/index.html', context)
