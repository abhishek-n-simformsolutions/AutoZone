from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from .models import BankProfile


@receiver(post_save, sender=User)
def create_bank_profile(sender, instance, created, **kwargs):
    if instance.is_bank:
        try:
            instance.bankprofile
        except:
            BankProfile.objects.create(user=instance).save()



# @receiver(post_save, sender=User)
# def save_bank_profile(sender, instance, **kwargs):
#     if instance.is_bank:
#         instance.bankprofile.create_user()
