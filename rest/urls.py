from django.urls import path
from . import views

app_name = 'rest'
urlpatterns = [
    path('', views.RestEndpoint.as_view(), name='rest_endpoint'),
]
