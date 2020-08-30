# Generated by Django 3.0.7 on 2020-08-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200828_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dicomserver',
            name='ip',
        ),
        migrations.AddField(
            model_name='dicomserver',
            name='host',
            field=models.CharField(default='localhost', max_length=255),
            preserve_default=False,
        ),
    ]