from django.urls import path
from products.views import (
    CategoriesView, ProductsView, ProductView, ChangeOfferView,
    FavoriteProductsView, RemoveFavoriteView, AddFavoriteView,
    ProductsJsonView
)


urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('products/', ProductsView.as_view(), name='products'),
    path('favorite-products/', FavoriteProductsView.as_view(), name='favorite_products'),
    path('add-favorite/', AddFavoriteView.as_view(), name='add_favorite'),
    path('remove-favorite/', RemoveFavoriteView.as_view(), name='remove_favorite'),
    path('products/<product_slug>/', ProductView.as_view(), name='product'),
    path('change-offer/', ChangeOfferView.as_view(), name='change_offer'),
    path('products.json/', ProductsJsonView.as_view(), name='products_json'),
]
