import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .authy_api import send_verfication_code, verify_sent_code
from .forms import RegisterForm, PhoneVerificationForm
from .models import User


class HomepageView(TemplateView):
    template_name = 'homepage.html'


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
            return redirect(reverse_lazy('register_url'))
        data = json.loads(response.text)

        # print(response.status_code, response.reason)
        # print(response.text)
        # print(data['success'])
        if data['success'] == False:
            messages.add_message(self.request, messages.ERROR,
                            data['message'])
            return redirect(reverse_lazy('register_url'))
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
            # print(response.text)
            data = json.loads(response.text)

            if data['success'] == True:
                login(request, user)
                if user.phone_number_verified is False:
                    user.phone_number_verified = True
                    user.save()
                return redirect(reverse_lazy('homepage_url'))
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
            return render(request, template_name, {'user': user, 'form': form})
        except Exception as e:
            # print("e",e)
            return HttpResponse("Not Allowed")


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user=authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        print("userrrrr",user.is_new_cardealer)
        if not user.is_new_cardealer:
            return redirect(reverse_lazy('accounts:homepage_url'), permanent=True)
        else:
            return redirect(reverse_lazy('accounts:homepage_url'), permanent=True)
