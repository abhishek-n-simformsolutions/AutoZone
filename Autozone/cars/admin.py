from django.contrib import admin
from .models import CarCompany, CarModel, City, CarVarient, CarInstance
from like_system.models import LikeSystem, LikesTarget


# Register your models here
admin.site.register(City)
admin.site.register(CarCompany)
admin.site.register(CarModel)
admin.site.register(CarVarient)
admin.site.register(CarInstance)
# admin.site.register(LikesTarget)
# admin.site.register(LikeSystem)


