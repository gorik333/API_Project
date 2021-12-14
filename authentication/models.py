import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class.
    By inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, first_name, last_name, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if first_name is None:
            raise TypeError('Users must have a first name.')

        if last_name is None:
            raise TypeError('Users must have a last name.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email),
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(db_index=True, max_length=255, default='John')
    last_name = models.CharField(db_index=True, max_length=255, default='Doe')

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return '{1} {0}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 50 days into the future.
        """
        jwt_token = jwt.encode({
            'id': self.pk,
            'exp': datetime.utcnow() + timedelta(days=50)
        }, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token.decode('utf-8')
