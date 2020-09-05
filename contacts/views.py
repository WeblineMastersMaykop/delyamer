from django.shortcuts import render, get_object_or_404
from django.views import View
from contacts.models import ContactInfo, City, Social, Shop
from pages.models import Page


class ContactsView(View):
    def get(self, request):
        try:
            parents = Page.objects.get(action='contacts').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        context = {
            'parents': parents,
        }
        return render(request, 'contacts/contacts.html', context)


class ShopsView(View):
    def get(self, request):
        cities = City.objects.all()

        try:
            parents = Page.objects.get(action='shops').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()


        first_city = cities.first()

        context = {
            'cities': cities,
            'parents': parents,
            'first_city': first_city
        }
        return render(request, 'contacts/shops.html', context)

