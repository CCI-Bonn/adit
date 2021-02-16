from django.template import Library

register = Library()


@register.inclusion_tag("core/_job_detail_control_panel.html", takes_context=True)
def job_control_panel(context):
    return {
        "delete_url": "batch_query_job_delete",
        "verify_url": "batch_query_job_verify",
        "cancel_url": "batch_query_job_cancel",
        "resume_url": "batch_query_job_resume",
        "retry_url": "batch_query_job_retry",
        "user": context["user"],
        "job": context["job"],
    }
