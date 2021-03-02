from django.urls import path
from . import views

app_name='car_dealer'

urlpatterns=[
     path('homepage/', views.NewCarDealerHomepageView.as_view(), name='new-cardealer-homepage-url'),
     path('add-new-car-form/', views.AddNewCarCreationView.as_view(), name='add-new-car-url'),

]