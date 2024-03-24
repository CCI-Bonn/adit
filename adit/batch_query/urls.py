from django.urls import path

from adit_radis_shared.common.views import HtmxTemplateView

from .views import (
    BatchQueryJobCancelView,
    BatchQueryJobCreateView,
    BatchQueryJobDeleteView,
    BatchQueryJobDetailView,
    BatchQueryJobListView,
    BatchQueryJobRestartView,
    BatchQueryJobResumeView,
    BatchQueryJobRetryView,
    BatchQueryJobVerifyView,
    BatchQueryResultDownloadView,
    BatchQueryResultListView,
    BatchQueryTaskDeleteView,
    BatchQueryTaskDetailView,
    BatchQueryTaskKillView,
    BatchQueryTaskResetView,
    BatchQueryUpdatePreferencesView,
)

urlpatterns = [
    path(
        "update-preferences/",
        BatchQueryUpdatePreferencesView.as_view(),
    ),
    path(
        "help/",
        HtmxTemplateView.as_view(template_name="batch_query/_batch_query_help.html"),
        name="batch_query_help",
    ),
    path(
        "jobs/",
        BatchQueryJobListView.as_view(),
        name="batch_query_job_list",
    ),
    path(
        "jobs/new/",
        BatchQueryJobCreateView.as_view(),
        name="batch_query_job_create",
    ),
    path(
        "jobs/<int:pk>/",
        BatchQueryJobDetailView.as_view(),
        name="batch_query_job_detail",
    ),
    path(
        "jobs/<int:pk>/delete/",
        BatchQueryJobDeleteView.as_view(),
        name="batch_query_job_delete",
    ),
    path(
        "jobs/<int:pk>/verify/",
        BatchQueryJobVerifyView.as_view(),
        name="batch_query_job_verify",
    ),
    path(
        "jobs/<int:pk>/cancel/",
        BatchQueryJobCancelView.as_view(),
        name="batch_query_job_cancel",
    ),
    path(
        "jobs/<int:pk>/resume/",
        BatchQueryJobResumeView.as_view(),
        name="batch_query_job_resume",
    ),
    path(
        "jobs/<int:pk>/retry/",
        BatchQueryJobRetryView.as_view(),
        name="batch_query_job_retry",
    ),
    path(
        "jobs/<int:pk>/restart/",
        BatchQueryJobRestartView.as_view(),
        name="batch_query_job_restart",
    ),
    path(
        "jobs/<int:pk>/results/",
        BatchQueryResultListView.as_view(),
        name="batch_query_result_list",
    ),
    path(
        "jobs/<int:pk>/download/",
        BatchQueryResultDownloadView.as_view(),
        name="batch_query_result_download",
    ),
    path(
        "tasks/<int:pk>/",
        BatchQueryTaskDetailView.as_view(),
        name="batch_query_task_detail",
    ),
    path(
        "tasks/<int:pk>/delete/",
        BatchQueryTaskDeleteView.as_view(),
        name="batch_query_task_delete",
    ),
    path(
        "tasks/<int:pk>/kill/",
        BatchQueryTaskKillView.as_view(),
        name="batch_query_task_kill",
    ),
    path(
        "tasks/<int:pk>/reset/",
        BatchQueryTaskResetView.as_view(),
        name="batch_query_task_reset",
    ),
]
