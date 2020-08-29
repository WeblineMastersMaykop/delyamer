from django.urls import path
from contacts.views import ContactsView, ShopsView


urlpatterns = [
    path('', ContactsView.as_view(), name='contacts'),
    path('shops/', ShopsView.as_view(), name='shops'),
]
