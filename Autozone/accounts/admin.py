from django import forms
from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterForm
from .models import User

# class BankUserCreationForm(UserCreationForm):
#     is_bank = forms.BooleanField()
#     is_new_cardealer = forms.BooleanField()



class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('username',)
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Fields',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'phone_number', 'phone_number_verified', 'is_new_cardealer', 'is_bank', 'country_code',
                ),
            },
        ),
    )

admin.site.register(User, UserAdmin)