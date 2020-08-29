from django.urls import path
from products.views import CategoriesView, CategoryView


urlpatterns = [
    path('', CategoriesView.as_view(), name='categories'),
    path('<category_slug>/', CategoryView.as_view(), name='category'),
]
