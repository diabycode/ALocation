# Generated by Django 4.2.1 on 2023-11-13 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('local', '0004_alter_local_rent_price'),
        ('renter', '0015_delete_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('rent', 'Rent a local'), ('unrent', 'Unrent a local'), ('payment', 'Payment of rent')], max_length=20)),
                ('act_at', models.DateTimeField(auto_now_add=True)),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='local.local')),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='renter.renter')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('seen_at', models.DateTimeField(blank=True, null=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracks_and_activities.activity')),
            ],
        ),
    ]
