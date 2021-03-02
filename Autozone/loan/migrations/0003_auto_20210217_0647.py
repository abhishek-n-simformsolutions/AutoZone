# Generated by Django 3.1.5 on 2021-02-17 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan', '0002_auto_20210216_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankprofile',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='bankprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bankprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
