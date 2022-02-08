from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response

from app.models import ProjectAPIKey


class TestView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        """Retrieve a project based on the request API key."""
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        apikey = APIKey.objects.get_from_key(key)
        project_api_key = ProjectAPIKey.objects.filter(apikey=apikey).first()
        assert isinstance(project_api_key, ProjectAPIKey)
        print("project_api_key", project_api_key.project)
        return Response("ok")
