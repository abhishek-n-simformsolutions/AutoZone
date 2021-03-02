from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView

# Create your views here.
from cars.models import CarInstance
from twilio.rest import Client

from .forms import ApplyForLoanForm
from .models import LoanInstance, BankProfile


class ApplyForLoanView(CreateView):
    form_class = ApplyForLoanForm
    template_name = 'applyforloanform.html'
    # success_url = reverse_lazy('cars:my-registered-car-url')

    def form_valid(self, form):
        loaninstance = form.save(commit=False)
        id=self.kwargs['carinstance_id']
        print(id)
        loaninstance.carinstance = get_object_or_404(CarInstance, pk=id)
        loaninstance.appliyer=self.request.user
        loaninstance.save()
        return HttpResponseRedirect(reverse_lazy('cars:my-registered-car-url'))


class BankHomepageView(ListView):
    template_name = 'bankhomepage.html'
    model = LoanInstance
    context_object_name = 'loaninstancelist'

    def get_queryset(self):
        bankprofile=BankProfile.objects.get(user=self.request.user)
        return LoanInstance.objects.filter(loan_bank=bankprofile, approved=False, rejected=False)


class RejectedLoanListView(ListView):
    template_name = 'bankhomepage.html'
    model = LoanInstance
    context_object_name = 'loaninstancelist'

    def get_queryset(self):
        bankprofile=BankProfile.objects.get(user=self.request.user)
        return LoanInstance.objects.filter(loan_bank=bankprofile, approved=False, rejected=True)


class ApprovedLoanListView(ListView):
    template_name = 'bankhomepage.html'
    model = LoanInstance
    context_object_name = 'loaninstancelist'

    def get_queryset(self):
        bankprofile=BankProfile.objects.get(user=self.request.user)
        return LoanInstance.objects.filter(loan_bank=bankprofile, approved=True, rejected=False)


class RejectLoanView(RedirectView):
    def get(self, request, *args, **kwargs):
        loaninstance_id=kwargs.get('id')
        print('inreject',loaninstance_id)
        loaninstance=get_object_or_404(LoanInstance, pk=loaninstance_id)
        print(loaninstance)
        loaninstance.rejected=True
        loaninstance.save()
        return HttpResponseRedirect(reverse_lazy('loan:bank_homepage_url'))


class ApproveLoanView(RedirectView):
    def get(self, request, *args, **kwargs):
        loaninstance_id=kwargs.get('id')
        print(loaninstance_id)
        loaninstance = get_object_or_404(LoanInstance, pk=loaninstance_id)
        loaninstance.approved=True
        loaninstance.save()
        loan_approval_sms(loaninstance.appliyer.phone_number)
        return HttpResponseRedirect(reverse_lazy('loan:bank_homepage_url'))


def loan_approval_sms(appliyer_number):
    message_to_broadcast = (f'your request for loan has been approved.')
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    appliyer_number = '+91'+str(appliyer_number)
    client.messages.create(to=appliyer_number,
                           from_=settings.TWILIO_NUMBER,
                           body=message_to_broadcast)
    return