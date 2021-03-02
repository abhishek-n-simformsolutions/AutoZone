from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    path('homepage', views.HomepageView.as_view(), name='homepage_url'),
    path('register/', views.RegisterView.as_view(), name="register_url"),
    path('verify/', views.PhoneVerificationView, name="phone_verification_url"),
    path('login/', views.CustomLoginView.as_view(), name='login_url'),
    path('logout/', auth_views.LogoutView.as_view(next_page= reverse_lazy('accounts:homepage_url')),name='logout_url'),
    path('custom_password_reset/', views.CustomPasswordResetView.as_view(), name='custom_password_reset_url'),
    path('resetverify/', views.PasswordResetPhoneVerificationView, name="reset_phone_verification_url"),
    path('reset/<int:id>/', views.SetNewPassword.as_view(), name='set_new_password_url'),
]