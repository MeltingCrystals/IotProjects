# Generated by Django 3.2.12 on 2024-11-19 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='temperatureandhumiditydata',
            name='accelx',
            field=models.CharField(default=0.0, max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temperatureandhumiditydata',
            name='accely',
            field=models.CharField(default=0.0, max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temperatureandhumiditydata',
            name='accelz',
            field=models.CharField(default=0.0, max_length=7),
            preserve_default=False,
        ),
    ]
