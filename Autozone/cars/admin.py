from django.contrib import admin
from .models import CarCompany, CarModel, City, CarVarient, CarInstance

# Register your models here
admin.site.register(City)
admin.site.register(CarCompany)
admin.site.register(CarModel)
admin.site.register(CarVarient)
admin.site.register(CarInstance)


