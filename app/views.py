from django.http import JsonResponse
from git import Repo
import os
import subprocess
import json
from datetime import datetime
from django.shortcuts import render
from .models import Deployment

def home(request):
    return render(request, "index.html")

def start_pipeline(request):

    repo_url = request.GET.get('repo_url')

    if not repo_url:
        return JsonResponse({
            "error": "Repository URL is required"
        })

    try:

        repo_name = repo_url.split("/")[-1].replace(".git", "")

        clone_path = os.path.join(
            "cloned_repos",
            repo_name
        )

        # Clone repository
        if not os.path.exists(clone_path):

            Repo.clone_from(
                repo_url,
                clone_path
            )

        # Docker image name
        image_name = repo_name.lower()

        # Build Docker image
        build_command = f"docker build -t {image_name} {clone_path}"

        build_process = subprocess.run(
            build_command,
            shell=True,
            capture_output=True,
            text=True
        )

        if build_process.returncode != 0:

            return JsonResponse({
                "status": "error",
                "message": build_process.stderr
            })

        run_command = f"docker run -d {image_name}"

        run_process = subprocess.run(
            run_command,
            shell=True,
            capture_output=True,
            text=True
        )

        container_id = run_process.stdout.strip()

        logs_command = f"docker logs {container_id}"

        logs_process = subprocess.run(
            logs_command,
            shell=True,
            capture_output=True,
            text=True
        )

        output_logs = logs_process.stdout

        Deployment.objects.create(
    repo_name=repo_name,
    repo_url=repo_url,
    status="success",
    container_id=container_id,
    output=output_logs
)

        return JsonResponse({
            "status": "success",
            "message": "Pipeline executed successfully",
            "container_id": container_id,
            "output": output_logs
        })

    except Exception as e:

        return JsonResponse({
            "status": "error",
            "message": str(e)
        })