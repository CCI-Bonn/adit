# Generated by Django 3.0.7 on 2020-06-24 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_transfer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batchtransferrequest',
            options={'permissions': [('cancel_batchtransferjob', 'Can cancel batch transfer job')]},
        ),
    ]
