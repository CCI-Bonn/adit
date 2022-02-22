# Generated by Django 3.2.8 on 2022-02-22 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch_transfer', '0007_auto_20211123_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchtransfertask',
            name='batch_ids',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='batchtransferjob',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='batchtransfersettings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='batchtransfertask',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
