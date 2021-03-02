from django.contrib import admin

# Register your models here.
from .models import LoanInstance, BankProfile

admin.site.register(LoanInstance)

admin.site.register(BankProfile)
