from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from adit.core.models import DicomServer
from adit.core.validators import (
    no_backslash_char_validator,
    no_control_chars_validator,
    no_wildcard_chars_validator,
)

id_validators = [
    no_backslash_char_validator,
    no_control_chars_validator,
    no_wildcard_chars_validator,
]


class DicomExplorerQueryForm(forms.Form):
    server = forms.ModelChoiceField(queryset=DicomServer.objects.all())
    patient_id = forms.CharField(
        label="Patient ID",
        max_length=64,
        required=False,
        validators=id_validators,
    )
    study_uid = forms.CharField(
        label="Study Instance UID",
        max_length=64,
        required=False,
        validators=id_validators,
    )
    accession_number = forms.CharField(
        label="Accession Number",
        max_length=16,
        required=False,
        validators=id_validators,
    )
    series_uid = forms.CharField(
        label="Series Instance UID",
        max_length=64,
        required=False,
        validators=id_validators,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["server"].widget.attrs["class"] = "custom-select"

        self.helper = FormHelper(self)
        self.helper.form_method = "GET"
        self.helper.wrapper_class = "form-group row"
        self.helper.label_class = "col-md-2 col-form-label"
        self.helper.field_class = "col-md-10"
        self.helper.add_input(Submit("query", "Query"))