from chartjs.views.lines import BaseLineChartView
from django.db.models import Count
from django.db.models.functions import ExtractWeek, TruncMonth
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from accounts.models import User


class DashBoardView(TemplateView):
    template_name = 'dashboard_home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        qs=User.objects.all() \
            .annotate(month=TruncMonth("date_joined")) \
            .values("month") \
            .annotate(c=Count("id")) \
            .order_by("-month")
       # u = <QuerySet [{'month': datetime.date(2021, 2, 1), 'c': 4}]>
        data['months'] = [x['month'].month for x in qs]
        data['num_of_users'] = [x['c'] for x in qs ]
        print(data['months'], data['num_of_users'])
        return data




class LineChartJSONView(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        qs=User.objects.all() \
            .annotate(month=TruncMonth("date_joined")) \
            .values("month") \
            .annotate(c=Count("id")) \
            .order_by("-month")
        return [x['month'].month for x in qs]

    def get_data(self):
        """Return 3 datasets to plot."""
        qs=User.objects.all() \
            .annotate(month=TruncMonth("date_joined")) \
            .values("month") \
            .annotate(c=Count("id")) \
            .order_by("-month")
        return [[x['c'] for x in qs],]


line_chart = TemplateView.as_view(template_name='graph.html')
line_chart_json = LineChartJSONView.as_view()



