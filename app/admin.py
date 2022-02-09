from django.contrib import admin
from app.models import LogResult, Project, ProjectAPIKey
from jutil.admin import ModelAdminBase


class ProjectAdmin(ModelAdminBase):
    list_display = (
        "name",
        "active",
        "created"
    )

    list_filter = ("name",)


class ProjectAPIKeyAdmin(ModelAdminBase):
    list_display = (
        "project",
        "apikey",
        "created"
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectAPIKey, ProjectAPIKeyAdmin)
admin.site.register(LogResult, ModelAdminBase)
