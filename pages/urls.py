from django.urls import path
from pages.views import PageView


urlpatterns = [
    path('<page_slug>/', PageView.as_view(), name='page'),
]
