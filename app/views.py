from django.http import JsonResponse
from django.shortcuts import render
from git import Repo
from .models import Deployment
import os
import subprocess


def home(request):
    return render(request, "index.html")


def start_pipeline(request):

    repo_url = request.GET.get("repo_url")

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

        # Clone or Update Repository
        if not os.path.exists(clone_path):

            Repo.clone_from(
                repo_url,
                clone_path,
                depth=1
            )

        else:

            repo = Repo(clone_path)
            repo.remotes.origin.pull()

        image_name = repo_name.lower()


        check_image = subprocess.run(
            f"docker image inspect {image_name}",
            shell=True,
            capture_output=True,
            text=True
        )

        if check_image.returncode != 0:

            build_command = (
                f"docker build -t {image_name} {clone_path}"
            )

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

        subprocess.run(
            f"docker rm -f {image_name}",
            shell=True,
            capture_output=True,
            text=True
        )

        run_command = (
            f"docker run -d --name {image_name} {image_name}"
        )

        run_process = subprocess.run(
            run_command,
            shell=True,
            capture_output=True,
            text=True
        )

        if run_process.returncode != 0:

            return JsonResponse({
                "status": "error",
                "message": run_process.stderr
            })

        container_id = run_process.stdout.strip()

        
        logs_process = subprocess.run(
            f"docker logs {container_id}",
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