from django.contrib import admin
from .models import UserRequest


@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'first_name', 'last_name')
