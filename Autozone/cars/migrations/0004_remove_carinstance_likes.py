# Generated by Django 3.1.5 on 2021-02-15 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_auto_20210215_0323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carinstance',
            name='likes',
        ),
    ]