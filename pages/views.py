from django.shortcuts import render, get_object_or_404
from django.views import View
from pages.models import Page


class PageView(View):
    def get(self, request, page_slug):
        page = get_object_or_404(Page, slug=page_slug)

        parents = page.get_ancestors(ascending=False, include_self=False)

        template = 'pages/page.html'
        if page.action == 'dropdown':
            template = 'pages/dropdown.html'

        context = {
            'page': page,
            'parents': parents
        }
        return render(request, template, context)
