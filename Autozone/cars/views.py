from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from like_system.models import LikeSystem
from twilio.rest import Client

from .forms import RegisterOldCarForm
from .models import CarInstance, City, CarCompany


@method_decorator(login_required, name='dispatch')
class RegisterOldCar(CreateView):
    form_class = RegisterOldCarForm
    template_name = 'car-registration.html'
    model = CarInstance
    success_url = reverse_lazy('cars:my-registered-car-url')

    def form_valid(self, form):
        car_instance = form.save(commit=False)
        car_instance.added_by = self.request.user
        car_instance.save()

def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request, qs):
    # qs = CarInstance.objects.filter(added_by=user)
    # user = request.user
    car_model = request.GET.get('car_model')
    car_company = request.GET.get('car_company')
    car_city = request.GET.get('city')
    # price = request.GET.get('price')
    reg_year = request.GET.get('reg_year')
    transmission_type = request.GET.get('transmission')
    fuel_type = request.GET.get('fuel_type')
    # print(car_company,car_city,reg_year,transmission_type,fuel_type)

    if is_valid_queryparam(car_model) and car_model != 'Choose...':
        qs.filter(car_model__car_model_name=car_model)

    if is_valid_queryparam(car_company) and car_company != 'Choose...':
        qs=qs.filter(car_model__car_company__company_name=car_company)
        # print('car company',qs)

    if is_valid_queryparam(car_city) and car_city != 'Choose...':
        qs=qs.filter(city__city_name=car_city)
        # print('city',qs)

    if is_valid_queryparam(reg_year) and reg_year != 'Choose...':
        qs=qs.filter(reg_year=reg_year)
        # print('reg_year',qs)

    if is_valid_queryparam(transmission_type) and transmission_type != 'Choose...':
        qs=qs.filter(transmission_type=transmission_type)
        # print('transmission',qs)

    if is_valid_queryparam(fuel_type) and fuel_type != 'Choose...':
        qs=qs.filter(fuel_type=fuel_type)
        # print('fuel',qs)

    return qs

@method_decorator(login_required, name='dispatch')
class RegisteredCarListView(ListView):
    template_name = 'cars-list.html'
    model = CarInstance
    context_object_name = 'carinstancelist'

    def get_queryset(self):
        user = self.request.user
        qs = CarInstance.objects.filter(added_by=user)
        qs=filter(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(RegisteredCarListView, self).get_context_data(**kwargs)
        context['cities'] = City.objects.all()
        context['companies'] = CarCompany.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class BuyUsedCarListView(ListView):
    template_name = 'cars-list.html'
    model = CarInstance
    context_object_name = 'carinstancelist'

    def get_queryset(self):
        user = self.request.user
        qs = CarInstance.objects.filter(~Q(added_by=user))
        qs=filter(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(BuyUsedCarListView, self).get_context_data(**kwargs)
        context['cities'] = City.objects.all()
        context['companies'] = CarCompany.objects.all()
        return context


class RegisteredCarDetailView(DetailView):
    model = CarInstance
    context_object_name = 'carinstance'
    pk_url_kwarg = 'id'
    template_name = 'ncar-detail.html'
    extra_context = {'contact_flag': False}



@method_decorator(login_required, name='dispatch')
class UpdateUsedCarView(UpdateView):
    form_class = RegisterOldCarForm
    template_name = 'car-registration.html'
    model = CarInstance
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('cars:my-registered-car-url')


@method_decorator(login_required, name='dispatch')
class DeleteUsedCarView(DeleteView):
    template_name = 'delete_confirm.html'
    pk_url_kwarg = 'id'
    model = CarInstance
    success_url = reverse_lazy('cars:my-registered-car-url')


@login_required
def GetContactDetail(request, owner_number, carinstance_id):
    user = request.user
    message_to_broadcast = (f'{user.full_name} has shown interest in your car. you can contact them on {user.phone_number}')
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    owner_number = '+91'+str(owner_number)
    client.messages.create(to=owner_number,
                           from_=settings.TWILIO_NUMBER,
                           body=message_to_broadcast)
    carinstance=get_object_or_404(CarInstance, pk=carinstance_id)
    return render(request,'ncar-detail.html',{'carinstance': carinstance, 'contact_flag': True})

@method_decorator(login_required, name='dispatch')
class GetLikedCarsListView(ListView):
    template_name = 'cars-list.html'

    def get_queryset(self):
        user=self.request.user
        l=LikeSystem.objects.filter(user=user).only('object_id')
        return CarInstance.objects.filter(id__in=l)

