from django import forms

from .models import LoanInstance


class ApplyForLoanForm(forms.ModelForm):
    class Meta:
        model = LoanInstance
        fields = ('desired_amount', 'loan_bank', 'income', 'income_proof')