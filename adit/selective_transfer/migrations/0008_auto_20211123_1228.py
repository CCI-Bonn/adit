# Generated by Django 3.1.3 on 2021-11-23 12:28

import adit.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selective_transfer', '0007_auto_20211111_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selectivetransfertask',
            name='series_uid',
        ),
        migrations.AddField(
            model_name='selectivetransfertask',
            name='series_uids',
            field=models.JSONField(blank=True, null=True, validators=[adit.core.validators.validate_uids]),
        ),
    ]
