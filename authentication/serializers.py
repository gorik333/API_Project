from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from api.utils import validate_password, validate_email_domain, validate_first_name, validate_last_name
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    email = serializers.EmailField(max_length=100, validators=[validate_email, validate_email_domain])
    password = serializers.CharField(min_length=7, max_length=16, write_only=True, validators=[validate_password])
    first_name = serializers.CharField(max_length=100, validators=[validate_first_name])
    last_name = serializers.CharField(max_length=100, validators=[validate_last_name])

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request or response.
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    email = serializers.EmailField(max_length=100, validators=[validate_email, validate_email_domain])
    password = serializers.CharField(min_length=7, max_length=16, write_only=True, validators=[validate_password])
    first_name = serializers.EmailField(max_length=100, validators=[validate_first_name])
    last_name = serializers.EmailField(max_length=100, validators=[validate_last_name])

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'token',)
        # `read_only_fields` is an alternative for `read_only=True`.
        # We use `read_only_fields` because we don't need to specify anything else about the field.
        # The password field needed the `min_length` & `max_length` properties,
        # but that isn't the case for the token.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # remove the password field from the `validated_data` dictionary
        # before iterating over it.
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        # After everything has been updated we must explicitly save the model.
        instance.save()

        return instance
