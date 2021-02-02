from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('homepage', views.HomepageView.as_view(), name='homepage_url'),
    path('register/', views.RegisterView.as_view(), name="register_url"),
    path('verify/', views.PhoneVerificationView, name="phone_verification_url"),
    path('login/', views.CustomLoginView.as_view(), name='login_url'),
]