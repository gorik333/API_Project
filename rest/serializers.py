from django.core.validators import validate_email
from rest_framework import serializers
from api.utils import validate_email_domain, validate_password, validate_last_name, validate_first_name


class TestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, validators=[validate_email, validate_email_domain])
    password = serializers.CharField(min_length=7, max_length=16, validators=[validate_password])
    first_name = serializers.CharField(max_length=128, required=True, validators=[validate_first_name])
    last_name = serializers.CharField(max_length=128, required=True, validators=[validate_last_name])
