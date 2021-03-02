import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, ListView
from django.views.generic.base import View

from .authy_api import send_verfication_code, verify_sent_code
from .forms import RegisterForm, PhoneVerificationForm, CustomPasswordResetForm
from .models import User


# @method_decorator(login_required, name='dispatch')
from cars.models import CarInstance


class HomepageView(View):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        newcarinstancelist=CarInstance.objects.filter(is_new=True)
        carinstancelist=CarInstance.objects.filter(is_new=False)
        return render(request, 'homepage.html', {'newcarinstancelist': newcarinstancelist, 'carinstancelist': carinstancelist})


class RegisterView(SuccessMessageMixin, FormView):
    template_name = 'registration/signup.html'
    form_class = RegisterForm
    success_message = "One-Time password sent to your registered mobile number.\
                        The verification code is valid for 10 minutes."

    def form_valid(self, form):
        user = form.save()
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            response = send_verfication_code(user)
        except Exception as e:
            messages.add_message(self.request, messages.ERROR,
                                'verification code not sent. \n'
                                'Please re-register.')
            return redirect(reverse_lazy('accounts:register_url'))
        data = json.loads(response.text)

        if data['success'] == False:
            messages.add_message(self.request, messages.ERROR,
                            data['message'])
            return redirect(reverse_lazy('accounts:register_url'))
        else:
            kwargs = {'user': user}
            self.request.method = 'GET'
            return PhoneVerificationView(self.request, **kwargs)


def PhoneVerificationView(request, **kwargs):
    template_name = 'registration/phone_confirm.html'

    if request.method == "POST":
        username = request.POST['username']
        user = User.objects.get(username=username)
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            verification_code = request.POST['one_time_password']
            response = verify_sent_code(verification_code, user)
            data = json.loads(response.text)

            if data['success'] == True:
                login(request, user)
                if user.phone_number_verified is False:
                    user.phone_number_verified = True
                    user.save()
                return redirect(reverse_lazy('accounts:homepage_url'))
            else:
                messages.add_message(request, messages.ERROR,
                                data['message'])
                return render(request, template_name, {'user':user})
        else:
            context = {
                'user': user,
                'form': form,
            }
            return render(request, template_name, context)

    elif request.method == "GET":
        try:
            user = kwargs.get('user')
            form = PhoneVerificationForm()
            return render(request, template_name, {'user': user, 'form': form, 'pass_reset': False})
        except Exception as e:
            print('e',e)
            return HttpResponse("Not Allowed")


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = False

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_new_cardealer and not request.user.is_bank:
                return redirect(reverse_lazy('accounts:homepage_url'), permanent=True)
            elif request.user.is_bank and not request.user.is_new_cardealer:
                return redirect(reverse_lazy('loan:bank_homepage_url'), permanent=True)
            elif request.user.is_new_cardealer and not request.user.is_bank:
                return redirect(reverse_lazy('car_dealer:new-cardealer-homepage-url'), permanent=True)# change to car dealer homepage
            else:
                return HttpResponse('Not Valid user')
        return super(CustomLoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(self.request, user)
        if not user.is_new_cardealer and not user.is_bank:
            return redirect(reverse_lazy('accounts:homepage_url'), permanent=True)
        elif user.is_bank and not user.is_new_cardealer:
            return redirect(reverse_lazy('loan:bank_homepage_url'), permanent=True)
        elif user.is_new_cardealer and not user.is_bank:
            return redirect(reverse_lazy('car_dealer:new-cardealer-homepage-url'), permanent=True)# change to car dealer homepage
        else:
            return HttpResponse('Not Valid user')


class CustomPasswordResetView(FormView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/custompassword_reset_form.html'

    def form_valid(self, form):
        phone_number = self.request.POST['phone_number']
        user = get_object_or_404(User, phone_number=phone_number)
        print(user)
        try:
            response = send_verfication_code(user)
        except Exception as e:
            messages.add_message(self.request, messages.ERROR,
                                'verification code not sent. \n'
                                'Please re-try.')
            return redirect(reverse_lazy('accounts:custom_password_reset_url'))
        data = json.loads(response.text)
        print('data', data)
        if data['success'] == False:
            messages.add_message(self.request, messages.ERROR,
                            data['message'])
            return redirect(reverse_lazy('accounts:custom_password_reset_url'))
        else:
            kwargs = {'user': user}
            self.request.method = 'GET'
            print('here')
            return PasswordResetPhoneVerificationView(self.request, **kwargs)


def PasswordResetPhoneVerificationView(request, **kwargs):
    template_name = 'registration/phone_confirm.html'

    if request.method == "POST":
        username = request.POST['username']
        user = User.objects.get(username=username)
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            print('in valid')
            verification_code = request.POST['one_time_password']
            response = verify_sent_code(verification_code, user)
            data = json.loads(response.text)
            # print(data['success'])
            if data['success'] == True:
                return redirect(reverse_lazy('accounts:set_new_password_url', kwargs={'id': user.id}))
            else:
                messages.add_message(request, messages.ERROR,
                                data['message'])
                return render(request, template_name, {'user':user})
        else:
            context = {
                'user': user,
                'form': form,
            }
            return render(request, template_name, context)
    elif request.method == "GET":
        try:
            user = kwargs.get('user')
            form = PhoneVerificationForm()
            return render(request, template_name, {'user': user, 'form': form, 'pass_reset':True})
        except Exception as e:
            # print('e',e)
            return HttpResponse("Not Allowed")


class SetNewPassword(FormView):
    form_class = SetPasswordForm
    template_name = 'registration/custompassword_reset_confirm.html'
    success_url = reverse_lazy('accounts:homepage_url')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print('hereee')
        user = get_object_or_404(User, pk=self.kwargs.get('id'))
        kwargs['user'] = user
        return kwargs

