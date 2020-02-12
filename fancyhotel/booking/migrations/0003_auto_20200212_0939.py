# Generated by Django 3.0.3 on 2020-02-12 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20200212_0821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelroom',
            name='doubleBeds',
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='numberOfBeds',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]