from django.urls import path
from orders.views import (
    CartView, AddToCartView, RemoveFromCartView, ChangeQuantityView,
    OrderOneClickAddView, ChangeDeliveryView, OrderAddView, OrderDoneView,
    OrderFailView, AddPromocodeView, RemovePromocodeView
)


urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('order-one-click-add/', OrderOneClickAddView.as_view(), name='order_one_click_add'),
    path('order-add/', OrderAddView.as_view(), name='order_add'),
    path('done/<order_id>/', OrderDoneView.as_view(), name='order_done'),
    path('fail/<order_id>/', OrderFailView.as_view(), name='order_fail'),
    path('change-delivery/', ChangeDeliveryView.as_view(), name='change_delivey'),
    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('change-quantity/', ChangeQuantityView.as_view(), name='change_quantity'),
    path('add-promocode/', AddPromocodeView.as_view(), name='add_promocode'),
    path('remove-promocode/', RemovePromocodeView.as_view(), name='remove_promocode'),
]
