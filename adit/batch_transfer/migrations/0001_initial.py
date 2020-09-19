# Generated by Django 3.1.1 on 2020-09-08 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_transfer_locked', models.BooleanField(default=False)),
                ('batch_transfer_suspended', models.BooleanField(default=False)),
                ('batch_slot_begin_time', models.TimeField(default=datetime.time(22, 0))),
                ('batch_slot_end_time', models.TimeField(default=datetime.time(8, 0))),
                ('batch_timeout', models.IntegerField(default=3)),
            ],
            options={
                'verbose_name_plural': 'App settings',
            },
        ),
    ]