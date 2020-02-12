# Generated by Django 3.0.3 on 2020-02-12 08:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelroom',
            name='floor',
        ),
        migrations.RemoveField(
            model_name='hotelroom',
            name='numberOnFloor',
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='roomNumber',
            field=models.IntegerField(default=101, unique=True, validators=[django.core.validators.MinValueValidator(101, message='Room number must be three digits (i.e. 101)')]),
            preserve_default=False,
        ),
    ]