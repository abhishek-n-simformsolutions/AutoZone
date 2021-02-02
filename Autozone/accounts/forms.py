from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.utils.translation import ugettext as _


class RegisterForm(forms.ModelForm):
    phone_number = forms.IntegerField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    country_code = forms.IntegerField(initial='+91')

    MIN_LENGTH = 4

    class Meta:
        model = User
        fields = ['username','full_name', 'country_code', 'phone_number', 'password', 'confirm_password',]

    def clean_username(self):
        username = self.data.get('username')
        return username

    def clean_password(self):
        password = self.data.get('password')
        validate_password(password)
        if password != self.data.get('confirm_password'):
            raise forms.ValidationError(_("Passwords do not match"))
        return password

    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                _("Another user with this phone number already exists"))
        return phone_number

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        user.set_password(self.cleaned_data['password'])
        print('Saving user with country_code', user.country_code)
        user.save()
        return user


class PhoneVerificationForm(forms.Form):
    one_time_password = forms.IntegerField()

    class Meta:
        fields = ['one_time_password', ]
