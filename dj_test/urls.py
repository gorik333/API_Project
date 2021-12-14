from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('rest/', include('rest.urls')),
    path('authentication/', include('authentication.urls', namespace='authentication')),
]
