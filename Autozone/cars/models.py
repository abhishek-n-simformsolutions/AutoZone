from PIL import Image
from django.conf import settings
from django.db import models
# Create your models here.
from accounts.models import User
from like_system.models import LikesTarget


class City(models.Model):
    city_name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('city_name',)
        verbose_name = 'city'

    def __str__(self):
        return self.city_name


class CarCompany(models.Model):
    company_name = models.CharField(max_length=50, unique=True)
    company_logo = models.ImageField(null=True, blank=True, upload_to='media/company-logo')

    class Meta:
        ordering = ['company_name', ]
        verbose_name = 'Car Company'

    def __str__(self):
        return self.company_name


class CarModel(models.Model):
    car_model_name = models.CharField(max_length=50, unique=True)
    car_company = models.ForeignKey(CarCompany, on_delete=models.CASCADE)

    class Meta:
        ordering = ['car_company','car_model_name']
        verbose_name ='Car Model'

    def __str__(self):
        return f'{ self.car_model_name }-{ self.car_company.company_name }'


class CarVarient(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    Varient_name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('car_model__car_company', 'car_model__car_model_name',)

    def __str__(self):
        return f'{self.Varient_name}-{self.car_model.car_model_name}'


class CarInstance(LikesTarget):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_varient = models.ForeignKey(CarVarient, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    km_driven = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/car-image')
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    FUEL_TYPE = (
        ('p', 'Petrol'),
        ('d', 'Deisel'),
        ('g', 'Gas'),
    )
    fuel_type = models.CharField(
        max_length=1,
        choices=FUEL_TYPE,
        default='p',
    )
    TRANSMISSION = (
        ('m', 'manual'),
        ('a', 'automatic'),
    )
    transmission_type = models.CharField(
        max_length=1,
        choices=TRANSMISSION,
        default='m'
    )
    REGISTRATION_YEAR = (
        ('a', '2010'),
        ('b', '2011'),
        ('c', '2012'),
        ('d', '2013'),
        ('e', '2014'),
        ('f', '2015'),
        ('g', '2016'),
        ('h', '2017'),
        ('i', '2018'),
        ('j', '2019'),
        ('k', '2020'),
        ('l', '2021'),
    )
    reg_year = models.CharField(
        max_length=1,
        choices=REGISTRATION_YEAR,
        default='l',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    mileage = models.PositiveIntegerField(blank=True)
    is_new = models.BooleanField(default=False)

    # likes=models.ManyToManyField(User,blank=True, related_name='likes')


    def __str__(self):
        return f'{self.get_reg_year_display()}-{self.car_model}'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)  # saving image at the same path

        if self.image1:
            img = Image.open(self.image1.path)

            if img.height > 300 or img.width > 300:
                new_img = (300, 300)
                img.thumbnail(new_img)
                img.save(self.image1.path)  # saving image at the same path

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['created_at', 'city', 'car_model__car_company', 'car_model__car_model_name']


# class Likes(models.Model):
#     liked_car_id = models.ForeignKey(CarInstance, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)