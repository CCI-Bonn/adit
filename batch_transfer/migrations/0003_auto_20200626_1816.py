# Generated by Django 3.0.7 on 2020-06-26 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch_transfer', '0002_auto_20200626_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='batchtransferitem',
            old_name='request_id',
            new_name='row_id',
        ),
        migrations.AlterUniqueTogether(
            name='batchtransferitem',
            unique_together={('row_id', 'job')},
        ),
    ]