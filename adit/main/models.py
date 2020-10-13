from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from model_utils.managers import InheritanceManager
from .site import job_type_choices
from .utils.dicom_connector import DicomConnector
from .fields import SeparatedValuesField


class AppSettings(models.Model):
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "App settings"


class DicomNode(models.Model):
    NODE_TYPE = None

    class NodeType(models.TextChoices):
        SERVER = "SV", "Server"
        FOLDER = "FO", "Folder"

    node_type = models.CharField(max_length=2, choices=NodeType.choices)
    name = models.CharField(unique=True, max_length=64)
    active = models.BooleanField(default=True)
    objects = InheritanceManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.node_type:
            if not self.NODE_TYPE in dict(self.NodeType.choices):
                raise AssertionError(f"Invalid node type: {self.NODE_TYPE}")
            self.node_type = self.NODE_TYPE

    def __str__(self):
        node_types_dict = dict(self.NodeType.choices)
        return f"DICOM {node_types_dict[self.node_type]} {self.name}"


class DicomServer(DicomNode):
    NODE_TYPE = DicomNode.NodeType.SERVER

    ae_title = models.CharField(unique=True, max_length=16)
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65535)]
    )
    patient_root_find_support = models.BooleanField(default=True)
    patient_root_get_support = models.BooleanField(default=True)
    patient_root_move_support = models.BooleanField(default=True)
    study_root_find_support = models.BooleanField(default=True)
    study_root_get_support = models.BooleanField(default=True)
    study_root_move_support = models.BooleanField(default=True)

    def create_connector(self, auto_connect=True):
        return DicomConnector(
            DicomConnector.Config(
                client_ae_title=settings.ADIT_AE_TITLE,
                server_ae_title=self.ae_title,
                server_host=self.host,
                server_port=self.port,
                patient_root_find_support=self.patient_root_find_support,
                patient_root_get_support=self.patient_root_get_support,
                patient_root_move_support=self.patient_root_move_support,
                study_root_find_support=self.study_root_find_support,
                study_root_get_support=self.study_root_get_support,
                study_root_move_support=self.study_root_move_support,
                auto_connect=auto_connect,
            )
        )

    def __str__(self):
        return f"DICOM Server {self.name}"


class DicomFolder(DicomNode):
    NODE_TYPE = DicomNode.NodeType.FOLDER

    path = models.CharField(max_length=256)


class TransferJob(models.Model):
    JOB_TYPE = None

    class Status(models.TextChoices):
        UNVERIFIED = "UV", "Unverified"
        PENDING = "PE", "Pending"
        IN_PROGRESS = "IP", "In Progress"
        CANCELING = "CI", "Canceling"
        CANCELED = "CA", "Canceled"
        SUCCESS = "SU", "Success"
        WARNING = "WA", "Warning"
        FAILURE = "FA", "Failure"

    class Meta:
        indexes = [models.Index(fields=["owner", "status"])]

    job_type = models.CharField(max_length=2, choices=job_type_choices)
    source = models.ForeignKey(DicomNode, related_name="+", on_delete=models.PROTECT)
    destination = models.ForeignKey(
        DicomNode, related_name="+", on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.UNVERIFIED
    )
    message = models.TextField(blank=True, null=True)
    trial_protocol_id = models.CharField(null=True, blank=True, max_length=64)
    trial_protocol_name = models.CharField(null=True, blank=True, max_length=64)
    archive_password = models.CharField(null=True, blank=True, max_length=50)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transfer_jobs"
    )
    created = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    objects = InheritanceManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.job_type:
            if not any(self.JOB_TYPE == job_type[0] for job_type in job_type_choices):
                raise AssertionError(f"Invalid job type: {self.JOB_TYPE}")
            self.job_type = self.JOB_TYPE

    def get_processed_tasks(self):
        non_processed = (TransferTask.Status.PENDING, TransferTask.Status.IN_PROGRESS)
        return self.tasks.exclude(status__in=non_processed)

    def is_deletable(self):
        return self.status in (self.Status.UNVERIFIED, self.Status.PENDING)

    def is_cancelable(self):
        return self.status in (self.Status.IN_PROGRESS,)

    def is_verified(self):
        return self.status != self.Status.UNVERIFIED

    def get_absolute_url(self):
        return reverse("transfer_job_detail", args=[str(self.id)])

    def __str__(self):
        status_dict = dict(self.Status.choices)
        return f"{self.__class__.__name__} {status_dict[self.status]}"


class TransferTask(models.Model):
    class Status(models.TextChoices):
        PENDING = "PE", "Pending"
        IN_PROGRESS = "IP", "In Progress"
        CANCELED = "CA", "Canceled"
        SUCCESS = "SU", "Success"
        FAILURE = "FA", "Failure"

    # The generic relation is optional and may be used to organize
    # the transfers in an additional way
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    job = models.ForeignKey(TransferJob, on_delete=models.CASCADE, related_name="tasks")
    patient_id = models.CharField(max_length=64)
    study_uid = models.CharField(max_length=64)
    series_uids = SeparatedValuesField(null=True, blank=True)
    pseudonym = models.CharField(null=True, blank=True, max_length=64)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )
    message = models.TextField(null=True, blank=True)
    log = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
