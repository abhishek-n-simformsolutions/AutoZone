from django.urls import path
from . import views

app_name = 'loan'

urlpatterns = [
    path('apply-for-loan/<int:carinstance_id>/', views.ApplyForLoanView.as_view(), name='apply-for-loan-url'),
    path('bank-homepage/', views.BankHomepageView.as_view(), name='bank_homepage_url'),
    path('Approved-Loans/', views.ApprovedLoanListView.as_view(), name='approved_loanpage_url'),
    path('Rejected-Loans/', views.RejectedLoanListView.as_view(), name='rejected_loanpage_url'),
    path('reject-loan/<int:id>/', views.RejectLoanView.as_view(), name='reject_loan_url'),
    path('Approve-loan/<int:id>/', views.ApproveLoanView.as_view(), name='approve_loan_url'),

]




