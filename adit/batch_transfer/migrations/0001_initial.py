# Generated by Django 3.1.2 on 2020-10-15 16:28

import adit.main.validators
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchTransferJob',
            fields=[
                ('transferjob_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.transferjob')),
                ('project_name', models.CharField(max_length=150)),
                ('project_description', models.TextField(max_length=2000)),
            ],
            bases=('main.transferjob',),
        ),
        migrations.CreateModel(
            name='BatchTransferSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locked', models.BooleanField(default=False)),
                ('suspended', models.BooleanField(default=False)),
                ('batch_slot_begin_time', models.TimeField(default=datetime.time(22, 0), help_text='Uses time zone of SERVER_ZIME_ZONE env.')),
                ('batch_slot_end_time', models.TimeField(default=datetime.time(8, 0), help_text='Uses time zone of SERVER_ZIME_ZONE env.')),
                ('batch_timeout', models.IntegerField(default=3)),
            ],
            options={
                'verbose_name_plural': 'Batch transfer settings',
            },
        ),
        migrations.CreateModel(
            name='BatchTransferRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_key', models.PositiveIntegerField()),
                ('patient_id', models.CharField(blank=True, max_length=64)),
                ('patient_name', models.CharField(blank=True, max_length=324)),
                ('patient_birth_date', models.DateField(blank=True, null=True)),
                ('accession_number', models.CharField(blank=True, max_length=16)),
                ('study_date', models.DateField(blank=True, null=True)),
                ('modality', models.CharField(blank=True, max_length=16)),
                ('pseudonym', models.CharField(blank=True, max_length=64, validators=[adit.main.validators.validate_pseudonym])),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('IP', 'In Progress'), ('CA', 'Canceled'), ('SU', 'Success'), ('FA', 'Failure')], default='PE', max_length=2)),
                ('message', models.TextField(blank=True, default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='batch_transfer.batchtransferjob')),
            ],
            options={
                'unique_together': {('row_key', 'job')},
            },
        ),
    ]
