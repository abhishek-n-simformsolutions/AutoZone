from PIL import Image
from django.db import models
# Create your models here.
from cars.models import CarInstance
from accounts.models import User


class BankProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bankprofile')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user}'


class LoanInstance(models.Model):
    carinstance = models.ForeignKey(CarInstance, on_delete=models.CASCADE)
    appliyer= models.ForeignKey(User, on_delete=models.CASCADE)
    desired_amount= models.PositiveIntegerField()
    loan_bank = models.ForeignKey(BankProfile, on_delete=models.CASCADE) #add loan bank
    income = models.PositiveIntegerField()
    income_proof = models.ImageField(upload_to='media/loan-document')
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.carinstance}-{self.appliyer}'

    def save(self):
        super().save()

        img = Image.open(self.income_proof.path)

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.income_proof.path)  # saving image at the same path



