from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from cars.models import CarInstance
from loan.models import LoanInstance

from cars.forms import RegisterOldCarForm


class NewCarDealerHomepageView(ListView):
    template_name = 'newcardealerhomepage.html'
    model = CarInstance
    context_object_name = 'carinstancelist'

    def get_queryset(self):
        user = self.request.user
        qs = CarInstance.objects.filter(added_by=user)
        return qs


class AddNewCarCreationView(CreateView):
    template_name = 'car-registration.html'
    form_class = RegisterOldCarForm
    success_url = reverse_lazy('car_dealer:new-cardealer-homepage-url')

    def form_valid(self, form):
        carinstance = form.save(commit=False)
        carinstance.is_new = True
        carinstance.save()
