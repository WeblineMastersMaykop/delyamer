from django.shortcuts import render, get_object_or_404
from django.views import View
from products.models import Category, Product
from pages.models import Page


class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.filter(parent=None)

        try:
            parents = Page.objects.get(action='products').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        context = {
            'categories': categories,
            'parents': parents,
        }
        return render(request, 'products/categories.html', context)


class CategoryView(View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)

        try:
            parents = Page.objects.get(action='products').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        context = {
            'category': category,
            'parents': parents,
        }
        return render(request, 'products/category.html', context)
