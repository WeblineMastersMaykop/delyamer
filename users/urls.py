from django.urls import path
from users.views import (
    LoginView, RegisterView, ActivateView, LogoutView,
    ProfileView, ChangeEmailView, ChangePasswordView,
    DeleteUserView, CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetCompleteView, CustomPasswordResetConfirmView,
    UserActiveOdersView, UserFinishedOdersView, OrderDetailView
)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('change-email/<uidb64>/<token>/', ChangeEmailView.as_view(), name='change_email'),
    path('delete-user/', DeleteUserView.as_view(), name='delete_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('active-orders/', UserActiveOdersView.as_view(), name='active_orders'),
    path('finished-orders/', UserFinishedOdersView.as_view(), name='finished_orders'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
