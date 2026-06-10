from django.contrib import admin
from django.urls import path
from app.views import start_pipeline
from app.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path(
        'start-pipeline/',
        start_pipeline
    ),
]