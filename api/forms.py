from django import forms
from django.core.validators import validate_email

from .utils import validate_email_domain, validate_password, \
    validate_first_name, validate_last_name


class TestForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        required=True,
        validators=[validate_email, validate_email_domain],
    )

    password = forms.CharField(
        min_length=7,
        max_length=16,
        required=True,
        validators=[validate_password],
    )

    first_name = forms.CharField(required=True, validators=[validate_first_name],)
    last_name = forms.CharField(required=True, validators=[validate_last_name],)
