from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from app.models import LogResult, ProjectAPIKey
import subprocess
import os.path
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


class ProcessDeploy(ViewSet):
    permission_classes = [HasAPIKey]

    def list(self, request):
        return Response("Try POST")

    def post(self, request):  # noqa
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        apikey = APIKey.objects.get_from_key(key)
        project_api_key = ProjectAPIKey.objects.filter(apikey=apikey).first()
        assert isinstance(project_api_key, ProjectAPIKey)
        print("project_api_key", project_api_key.project)
        project = project_api_key.project
        if not project.active:
            return Response({"result": "the project is inactive", "status": 400})
        script_path = project.script_path

        if not os.path.isfile(script_path):
            return Response({"result": f"Script path {script_path} is not found", "status": 400})
        try:
            process = subprocess.Popen(
                ["bash", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            streamdata = process.communicate()[0]
            out = str(streamdata)
            log = LogResult(content=out, status_code=process.returncode, project=project)
            log.save()

            check_status = log.status_code == 0
            if project.success_text:
                check_status = check_status and project.success_text in out
            result = "success" if check_status else "fail"
            domain = request.scheme + "://" + request.META["HTTP_HOST"]
            log_url = domain + reverse(
                "view_log",
                args=(
                    log.id,
                    log.view_token,
                ),
            )
            return Response({"result": result, "log_url": log_url})

        except Exception as error:
            print(f"Something else went wrong with error {error}")
            log = LogResult(content=str(error), status_code=1, project=project)
            log.save()
            log_url = domain + reverse(
                "view_log",
                args=(
                    log.id,
                    log.view_token,
                ),
            )
            return Response({"result": "fail", "url": log_url})


def view_log(request, log_id, view_token):
    try:
        log = LogResult.objects.get(pk=log_id, view_token=view_token)
        return render(request, "app/view_log.html", {"log": log})
    except LogResult.DoesNotExist:  # pylint: disable=no-member
        return HttpResponse(_("invalid request"))


DEFAULT_ROUTES = [
    ("process-deploy", ProcessDeploy),
]
