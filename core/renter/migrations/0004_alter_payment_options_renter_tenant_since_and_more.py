# Generated by Django 4.2.1 on 2023-07-29 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renter', '0003_alter_payment_paid_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Paiement', 'verbose_name_plural': 'Paiements'},
        ),
        migrations.AddField(
            model_name='renter',
            name='tenant_since',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid_at',
            field=models.DateField(null=True),
        ),
    ]
