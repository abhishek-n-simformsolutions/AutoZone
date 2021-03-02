from django.urls import path

from . import views

app_name = 'cars'
urlpatterns = [
    path('register-old-car/', views.RegisterOldCar.as_view(), name='register-old-car-url'),
    path('my-registered-cars/', views.RegisteredCarListView.as_view(), name='my-registered-car-url'),
    path('my-registered-cars/<int:id>/', views.RegisteredCarDetailView.as_view(), name='my-registered-car-detail-url'),
    path('buy-used-car/', views.BuyUsedCarListView.as_view(), name='buy-used-car'),
    path('update/<int:id>/', views.UpdateUsedCarView.as_view(), name='update-used-car-url'),
    path('delete/<int:id>/',  views.DeleteUsedCarView.as_view(), name='delete-used-car-url'),
    path('get-contact-detail/<int:owner_number>/<int:carinstance_id>/', views.GetContactDetail, name='get-contact-detail-url'),

]

