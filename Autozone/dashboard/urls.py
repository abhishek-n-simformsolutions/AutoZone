from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('api/chart/data/', views.DashBoardView.as_view(),name='dashboard-url'),
    path('chart/', views.line_chart, name='line_chart'),
    path('chartJSON', views.line_chart_json, name='line_chart_json'),
]


