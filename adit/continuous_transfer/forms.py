from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import ContinuousTransferJob, DataElementFilter


class DateInput(forms.DateInput):
    input_type = "date"


class ContinuousTransferJobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit("save", "Create Job"))

    class Meta:
        model = ContinuousTransferJob
        fields = (
            "source",
            "destination",
            "project_name",
            "project_description",
            "trial_protocol_id",
            "trial_protocol_name",
            "start_date",
            "end_date",
        )
        widgets = {"start_date": DateInput(), "end_date": DateInput()}


class DataElementFilterForm(forms.ModelForm):
    class Meta:
        model = DataElementFilter
        fields = ("dicom_tag", "filter_type", "filter_value", "case_sensitive")


DataElementFilterFormSet = forms.inlineformset_factory(
    ContinuousTransferJob, DataElementFilter, form=DataElementFilterForm, extra=1
)