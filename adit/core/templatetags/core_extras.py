from django.template import Library
from ..models import TransferJob, TransferTask

register = Library()


@register.filter
def transfer_job_status_css_class(status):
    text_class = ""
    if status == TransferJob.Status.UNVERIFIED:
        text_class = "text-info"
    elif status == TransferJob.Status.PENDING:
        text_class = "text-secondary"
    elif status == TransferJob.Status.IN_PROGRESS:
        text_class = "text-info"
    elif status == TransferJob.Status.CANCELING:
        text_class = "text-muted"
    elif status == TransferJob.Status.CANCELED:
        text_class = "text-muted"
    elif status == TransferJob.Status.SUCCESS:
        text_class = "text-success"
    elif status == TransferJob.Status.WARNING:
        text_class = "text-warning"
    elif status == TransferJob.Status.FAILURE:
        text_class = "text-danger"
    return text_class


@register.filter
def transfer_task_status_css_class(status):
    text_class = ""
    if status == TransferTask.Status.PENDING:
        text_class = "text-secondary"
    elif status == TransferTask.Status.IN_PROGRESS:
        text_class = "text-info"
    elif status == TransferTask.Status.CANCELED:
        text_class = "text-muted"
    elif status == TransferTask.Status.SUCCESS:
        text_class = "text-success"
    elif status == TransferTask.Status.FAILURE:
        text_class = "text-danger"
    return text_class