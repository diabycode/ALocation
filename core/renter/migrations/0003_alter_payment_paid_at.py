# Generated by Django 4.2.1 on 2023-07-29 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renter', '0002_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
