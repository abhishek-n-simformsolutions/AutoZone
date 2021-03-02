from django.db.models.signals import post_save
from django.dispatch import receiver

from car_dealer.models import User
from .models import NewCarDealerProfile


@receiver(post_save, sender=User)
def create_newcardealer_profile(sender, instance, created, **kwargs):
    if instance.is_new_cardealer:
        try:
            instance.newcardealerprofile
        except:
            NewCarDealerProfile.objects.create(user=instance).save()
