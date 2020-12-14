from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from adit.core.models import AppSettings, TransferJob, TransferTask
from adit.core.validators import (
    no_backslash_char_validator,
    no_control_chars_validator,
    no_wildcard_chars_validator,
)


class BatchTransferSettings(AppSettings):
    class Meta:
        verbose_name_plural = "Batch transfer settings"


class BatchTransferJob(TransferJob):
    project_name = models.CharField(max_length=150)
    project_description = models.TextField(max_length=2000)

    def get_processed_requests(self):
        non_processed = (
            BatchTransferRequest.Status.PENDING,
            BatchTransferRequest.Status.IN_PROGRESS,
        )
        return self.requests.exclude(status__in=non_processed)

    def delay(self):
        from .tasks import batch_transfer  # pylint: disable=import-outside-toplevel

        batch_transfer.delay(self.id)

    def get_absolute_url(self):
        return reverse("batch_transfer_job_detail", args=[str(self.id)])


class BatchTransferRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PE", "Pending"
        IN_PROGRESS = "IP", "In Progress"
        CANCELED = "CA", "Canceled"
        SUCCESS = "SU", "Success"
        WARNING = "WA", "Warning"
        FAILURE = "FA", "Failure"

    class Meta:
        unique_together = ("row_number", "job")
        ordering = ("row_number",)

    job = models.ForeignKey(
        BatchTransferJob, on_delete=models.CASCADE, related_name="requests"
    )
    row_number = models.PositiveIntegerField()
    patient_id = models.CharField(
        blank=True,
        max_length=64,
        validators=[
            no_backslash_char_validator,
            no_control_chars_validator,
            no_wildcard_chars_validator,
        ],
    )
    patient_name = models.CharField(
        blank=True,
        max_length=324,
        validators=[
            no_backslash_char_validator,
            no_control_chars_validator,
            no_wildcard_chars_validator,
        ],
    )
    patient_birth_date = models.DateField(
        null=True,
        blank=True,
        error_messages={"invalid": "Invalid date format."},
    )
    accession_number = models.CharField(
        blank=True,
        max_length=16,
        validators=[
            no_backslash_char_validator,
            no_control_chars_validator,
            no_wildcard_chars_validator,
        ],
    )
    study_date = models.DateField(
        null=True,
        blank=True,
        error_messages={"invalid": "Invalid date format."},
    )
    modality = models.CharField(
        blank=True,
        max_length=16,
        validators=[
            no_backslash_char_validator,
            no_control_chars_validator,
            no_wildcard_chars_validator,
        ],
    )
    pseudonym = models.CharField(
        blank=True,
        max_length=64,
        validators=[
            no_backslash_char_validator,
            no_control_chars_validator,
            no_wildcard_chars_validator,
        ],
    )
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PENDING
    )
    message = models.TextField(blank=True, default="")
    created = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def clean(self):
        errors = []

        if not (self.patient_id or self.patient_name and self.patient_birth_date):
            errors.append(
                ValidationError(
                    "A patient must be identifiable by either a 'Patient ID' "
                    "or a 'Patient Name' combined with a 'Birth Date'."
                )
            )

        if not (self.accession_number or self.study_date and self.modality):
            errors.append(
                ValidationError(
                    "A study must be identifiable by either an 'Accession Number' "
                    "or a 'Study Date' combined with a 'Modality'."
                )
            )

        if len(errors) > 0:
            raise ValidationError(errors)


class BatchTransferTask(TransferTask):
    job = models.ForeignKey(
        BatchTransferJob,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    request = models.ForeignKey(
        BatchTransferRequest,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    def get_absolute_url(self):
        return reverse("batch_transfer_task_detail", args=[str(self.id)])
