# Generated by Django 3.0.7 on 2020-07-17 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch_transfer', '0007_auto_20200716_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsettings',
            name='batch_timeout',
            field=models.IntegerField(default=0),
        ),
    ]