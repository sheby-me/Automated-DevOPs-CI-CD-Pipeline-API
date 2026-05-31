from django.contrib import admin
from django.urls import path
from app.views import start_pipeline

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'start-pipeline/',
        start_pipeline
    ),
]