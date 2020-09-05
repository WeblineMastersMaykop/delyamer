from django.urls import path
from products.views import CategoriesView, ProductsView, ProductView


urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<product_slug>/', ProductView.as_view(), name='product'),
]
