"""Autozone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('like/', include('like_system.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('accounts:homepage_url'))),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('cars/', include('cars.urls', namespace='cars')),
    path('loan/', include('loan.urls', namespace='loan')),
    path('new-car-dealer/', include('car_dealer.urls', namespace='car_dealer')),
    path('dashboard/',include('dashboard.urls', namespace='dashboard')),
    path('__debug__/', include(debug_toolbar.urls)),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

