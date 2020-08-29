from django.shortcuts import render, get_object_or_404
from django.views import View
from contacts.models import ContactInfo, City
from pages.models import Page


class ContactsView(View):
    def get(self, request):
        contact_info = ContactInfo.objects.first()

        try:
            parents = Page.objects.get(action='contacts').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        context = {
            'contact_info': contact_info,
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

        context = {
            'cities': cities,
            'parents': parents,
        }
        return render(request, 'contacts/shops.html', context)

