# Generated by Django 3.1.5 on 2021-02-16 05:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_carinstance_mileage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desired_amount', models.PositiveIntegerField()),
                ('income', models.PositiveIntegerField()),
                ('income_proof', models.FileField(upload_to='media/loan-document')),
                ('approved', models.BooleanField(default=False)),
                ('appliyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('carinstance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.carinstance')),
                ('loan_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.bankprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='Loan',
        ),
    ]
