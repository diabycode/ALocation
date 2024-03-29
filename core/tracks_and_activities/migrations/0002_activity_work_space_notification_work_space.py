# Generated by Django 4.2.1 on 2023-11-21 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
        ('tracks_and_activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='work_space',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workspace.workspace'),
        ),
        migrations.AddField(
            model_name='notification',
            name='work_space',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workspace.workspace'),
        ),
    ]
