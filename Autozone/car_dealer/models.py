from django.db import models

# Create your models here.
from accounts.models import User


class NewCarDealerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='newcardealerprofile')

    def __str__(self):
        return f'{self.user.username}'
