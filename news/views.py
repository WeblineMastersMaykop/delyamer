from django.shortcuts import render, get_object_or_404
from django.views import View
from news.models import News
from pages.models import Page
from core.paginator import pagination


class NewsView(View):
    def get(self, request):
        news = News.objects.filter(is_active=True).select_related('category')

        try:
            parents = Page.objects.get(action='news').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        page_number = request.GET.get('page', 1)
        pag_res = pagination(news, page_number, request.GET.copy())

        context = {
            'news': news,
            'parents': parents,

            'page_object': pag_res['page'],
            'is_paginated': pag_res['is_paginated'],
            'next_url': pag_res['next_url'],
            'prev_url': pag_res['prev_url'],
        }
        return render(request, 'news/news.html', context)


class NewsDetailView(View):
    def get(self, request, news_slug):
        news_item = get_object_or_404(News, slug=news_slug)

        try:
            parents = Page.objects.get(action='news').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        context = {
            'news_item': news_item,
            'parents': parents,
        }
        return render(request, 'news/news-detail.html', context)
