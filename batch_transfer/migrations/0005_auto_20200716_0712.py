# Generated by Django 3.0.7 on 2020-07-16 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_transfer', '0004_auto_20200716_0644'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SiteConfig',
            new_name='AppSettings',
        ),
    ]