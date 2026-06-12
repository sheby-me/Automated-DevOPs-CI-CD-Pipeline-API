from django.contrib import admin
from .models import Deployment

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):

    list_display = (
        'repo_name',
        'status',
        'container_id',
        'created_at'
    )

    search_fields = (
        'repo_name',
        'status'
    )

    list_filter = (
        'status',
    )