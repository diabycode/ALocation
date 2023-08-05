# Generated by Django 4.2.1 on 2023-08-02 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('renter', '0006_payment_local'),
        ('local', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='local',
            name='rented_since',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='local',
            name='current_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='renter.renter'),
        ),
    ]
