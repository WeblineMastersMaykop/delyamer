from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from contacts.models import ContactInfo, City, Social, Shop
from pages.models import Page
from contacts.forms import FeedBackForm
from core.models import MailFromString, MailToString


class ContactsView(View):
    def get(self, request):
        try:
            parents = Page.objects.get(action='contacts').get_ancestors(ascending=False, include_self=False)
        except:
            parents = Page.objects.none()

        fb_form = FeedBackForm()

        context = {
            'parents': parents,
            'fb_form': fb_form,
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


class FeedBackView(View):
    def post(self, request):
        fb_form = FeedBackForm(request.POST)
        status = 0

        if fb_form.is_valid():
            current_site = get_current_site(request)
            mail_subject = 'Новое сообщение на сайте: ' + current_site.domain
            message = render_to_string('contacts/feedback-message.html', {
                'domain': current_site.domain,
                'email_or_phone': request.POST.get('email_or_phone'),
                'name': request.POST.get('name'),
                'text': request.POST.get('text'),
            })
            to_email = [item.email for item in MailToString.objects.all()]
            from_email = MailFromString.objects.first().host_user
            email = EmailMessage(mail_subject, message, from_email=from_email, to=to_email)
            email.send()
            fb_form.save()
            status = 1
            
        context = {
            'status': status,
        }

        return JsonResponse(context)
