# Generated by Django 4.2.7 on 2023-11-12 15:28

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0009_remove_queuedtask_eta_priority_created_idx_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExampleAppSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("locked", models.BooleanField(default=False)),
                ("suspended", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExampleTransferJob",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("UV", "Unverified"),
                            ("PE", "Pending"),
                            ("IP", "In Progress"),
                            ("CI", "Canceling"),
                            ("CA", "Canceled"),
                            ("SU", "Success"),
                            ("WA", "Warning"),
                            ("FA", "Failure"),
                        ],
                        default="UV",
                        max_length=2,
                    ),
                ),
                ("urgent", models.BooleanField(default=False)),
                ("message", models.TextField(blank=True, default="")),
                ("send_finished_mail", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("start", models.DateTimeField(blank=True, null=True)),
                ("end", models.DateTimeField(blank=True, null=True)),
                (
                    "trial_protocol_id",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message="Contains invalid backslash character",
                                regex="\\\\",
                            )
                        ],
                    ),
                ),
                (
                    "trial_protocol_name",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message="Contains invalid backslash character",
                                regex="\\\\",
                            )
                        ],
                    ),
                ),
                ("archive_password", models.CharField(blank=True, max_length=50)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_jobs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("can_process_urgently", "Can process urgently"),
                    ("can_transfer_unpseudonymized", "Can transfer unpseudonymized"),
                ],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExampleTransferTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PE", "Pending"),
                            ("IP", "In Progress"),
                            ("CA", "Canceled"),
                            ("SU", "Success"),
                            ("WA", "Warning"),
                            ("FA", "Failure"),
                        ],
                        default="PE",
                        max_length=2,
                    ),
                ),
                ("retries", models.PositiveSmallIntegerField(default=0)),
                ("message", models.TextField(blank=True, default="")),
                ("log", models.TextField(blank=True, default="")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("start", models.DateTimeField(blank=True, null=True)),
                ("end", models.DateTimeField(blank=True, null=True)),
                (
                    "patient_id",
                    models.CharField(
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message="Contains invalid backslash character",
                                regex="\\\\",
                            ),
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message="Contains invalid control characters.",
                                regex="[\\f\\n\\r]",
                            ),
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message="Contains invalid wildcard characters.",
                                regex="[\\*\\?]",
                            ),
                        ],
                    ),
                ),
                (
                    "study_uid",
                    models.CharField(
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Invalid character in UID.", regex="^[\\d\\.]+$"
                            )
                        ],
                    ),
                ),
                (
                    "series_uids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            max_length=64,
                            validators=[
                                django.core.validators.RegexValidator(
                                    message="Invalid character in UID.", regex="^[\\d\\.]+$"
                                )
                            ],
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "pseudonym",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message="Contains invalid backslash character",
                                regex="\\\\",
                            ),
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message="Contains invalid control characters.",
                                regex="[\\f\\n\\r]",
                            ),
                        ],
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="core.dicomnode",
                    ),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="example_app.exampletransferjob",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="core.dicomnode",
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
                "abstract": False,
            },
        ),
        migrations.AddIndex(
            model_name="exampletransferjob",
            index=models.Index(fields=["owner", "status"], name="example_app_owner_i_090040_idx"),
        ),
    ]
