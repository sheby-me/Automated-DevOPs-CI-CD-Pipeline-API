from django.db import models

# Create your models here.

class Deployment(models.Model):

    repo_name = models.CharField(max_length=255)

    repo_url = models.URLField()

    status = models.CharField(max_length=50)

    container_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    output = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.repo_name