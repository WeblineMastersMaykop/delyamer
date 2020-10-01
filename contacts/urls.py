from django.urls import path
from contacts.views import ContactsView, ShopsView, FeedBackView


urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('shops/', ShopsView.as_view(), name='shops'),
    path('add-message/', FeedBackView.as_view(), name='feedback'),
]
