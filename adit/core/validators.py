from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

no_backslash_char_validator = RegexValidator(
    regex=r"\\",
    message="Contains invalid backslash character",
    inverse_match=True,
)


no_control_chars_validator = RegexValidator(
    regex=r"[\f\n\r]",
    message="Contains invalid control characters.",
    inverse_match=True,
)

no_wildcard_chars_validator = RegexValidator(
    regex=r"[\*\?]",
    message="Contains invalid wildcard characters.",
    inverse_match=True,
)

uid_chars_validator = RegexValidator(regex=r"^[\d\.]+$", message="Invalid character in UID.")


def validate_uid_list(value):
    if not isinstance(value, list):
        raise ValidationError("Must be a list of UIDs.")

    for uid in value:
        if not isinstance(uid, str):
            raise ValidationError("Invalid UID type.")

        if len(uid) > 64:
            raise ValidationError("UID string too long (max 64 characters).")

        uid_chars_validator(uid)


def validate_modalities(value):
    if not isinstance(value, list):
        raise ValidationError(f"Invalid modalities: {value} [{type(value)}]")

    for modality in value:
        if not isinstance(modality, str) or len(modality) > 16:
            raise ValidationError(f"Invalid modality: {modality} [{type(modality)}]")

        no_backslash_char_validator(modality)
        no_control_chars_validator(modality)
        no_wildcard_chars_validator(modality)


def validate_series_number(value):
    # Series Number uses a Value Representation (VR) of Integer String (IS)
    # https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    if not isinstance(value, str):
        raise ValidationError(f"Invalid type of series number: {value} [{type(value)}]")

    try:
        snr = int(value)
        if snr < -(2**31) or snr > 2**31 - 1:
            raise ValueError()
    except ValueError:
        raise ValidationError(f"Invalid series number: {value}")


def validate_series_numbers(value):
    if not isinstance(value, list):
        raise ValidationError(f"Invalid series numbers: {value} [{type(value)}]")

    for series_number in value:
        validate_series_number(series_number)
