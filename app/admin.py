from django.contrib import admin
from app.models import LogResult, Project, ProjectAPIKey, MaintenanceTime
from jutil.admin import ModelAdminBase
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.admin import APIKeyModelAdmin


class MaintenanceTimeInlineAdmin(admin.StackedInline):
    model = MaintenanceTime
    extra = 0


class ProjectAdmin(ModelAdminBase):
    list_display = ("name", "active", "created")
    list_filter = ("name",)
    inlines = [MaintenanceTimeInlineAdmin]


class LogResultAdmin(ModelAdminBase):
    list_display = ("project", "created", "status_code")


class ProjectAPIKeyInlineAdmin(admin.StackedInline):
    model = ProjectAPIKey
    can_delete = False
    min_num = 1
    max_num = 1
    readonly_fields = ("created",)
    raw_id_fields = ()
    fieldsets = (
        (
            None,
            {
                "fields": ["project"],
            },
        ),
    )


class CustomAPIKeyAdmin(APIKeyModelAdmin):
    inlines = (ProjectAPIKeyInlineAdmin,)


admin.site.unregister(APIKey)
admin.site.register(APIKey, CustomAPIKeyAdmin)

admin.site.register(Project, ProjectAdmin)
admin.site.register(LogResult, LogResultAdmin)
