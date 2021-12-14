from django.urls import path
from .views import get_requests, post_requests

app_name = 'api'
urlpatterns = [
    path('v1/get/', get_requests, name='get_request'),   # GET API
    path('v1/post/', post_requests, name='post_request')   # POST API
]
