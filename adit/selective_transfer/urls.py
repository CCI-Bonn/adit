from django.urls import path

from adit_radis_shared.common.views import HtmxTemplateView

from .views import (
    SelectiveTransferJobCancelView,
    SelectiveTransferJobCreateView,
    SelectiveTransferJobDeleteView,
    SelectiveTransferJobDetailView,
    SelectiveTransferJobListView,
    SelectiveTransferJobRestartView,
    SelectiveTransferJobResumeView,
    SelectiveTransferJobRetryView,
    SelectiveTransferJobVerifyView,
    SelectiveTransferTaskDeleteView,
    SelectiveTransferTaskDetailView,
    SelectiveTransferTaskKillView,
    SelectiveTransferTaskResetView,
    SelectiveTransferUpdatePreferencesView,
)

urlpatterns = [
    path(
        "update-preferences/",
        SelectiveTransferUpdatePreferencesView.as_view(),
    ),
    path(
        "help/",
        HtmxTemplateView.as_view(template_name="selective_transfer/_selective_transfer_help.html"),
        name="selective_transfer_help",
    ),
    path(
        "jobs/",
        SelectiveTransferJobListView.as_view(),
        name="selective_transfer_job_list",
    ),
    path(
        "jobs/new/",
        SelectiveTransferJobCreateView.as_view(),
        name="selective_transfer_job_create",
    ),
    path(
        "jobs/<int:pk>/",
        SelectiveTransferJobDetailView.as_view(),
        name="selective_transfer_job_detail",
    ),
    path(
        "jobs/<int:pk>/delete/",
        SelectiveTransferJobDeleteView.as_view(),
        name="selective_transfer_job_delete",
    ),
    path(
        "jobs/<int:pk>/verify/",
        SelectiveTransferJobVerifyView.as_view(),
        name="selective_transfer_job_verify",
    ),
    path(
        "jobs/<int:pk>/cancel/",
        SelectiveTransferJobCancelView.as_view(),
        name="selective_transfer_job_cancel",
    ),
    path(
        "jobs/<int:pk>/resume/",
        SelectiveTransferJobResumeView.as_view(),
        name="selective_transfer_job_resume",
    ),
    path(
        "jobs/<int:pk>/retry/",
        SelectiveTransferJobRetryView.as_view(),
        name="selective_transfer_job_retry",
    ),
    path(
        "jobs/<int:pk>/restart/",
        SelectiveTransferJobRestartView.as_view(),
        name="selective_transfer_job_restart",
    ),
    path(
        "tasks/<int:pk>/",
        SelectiveTransferTaskDetailView.as_view(),
        name="selective_transfer_task_detail",
    ),
    path(
        "tasks/<int:pk>/delete/",
        SelectiveTransferTaskDeleteView.as_view(),
        name="selective_transfer_task_delete",
    ),
    path(
        "tasks/<int:pk>/kill/",
        SelectiveTransferTaskKillView.as_view(),
        name="selective_transfer_task_kill",
    ),
    path(
        "tasks/<int:pk>/reset/",
        SelectiveTransferTaskResetView.as_view(),
        name="selective_transfer_task_reset",
    ),
]
