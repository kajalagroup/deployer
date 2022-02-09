from django.db import models
from rest_framework_api_key.models import APIKey
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
import uuid


class Project(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=128)
    script_path = models.CharField(verbose_name=_("script path"), max_length=256)
    active = models.BooleanField(verbose_name=_("active"), default=True)
    created = models.DateTimeField(
        verbose_name=_("created"),
        default=now,
        db_index=True,
        editable=False,
        blank=True,
    )

    def __str__(self):
        return self.name


class ProjectAPIKey(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
    apikey = models.OneToOneField(
        APIKey,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
    created = models.DateTimeField(
        verbose_name=_("created"),
        default=now,
        db_index=True,
        editable=False,
        blank=True,
    )


class LogResult(models.Model):
    status_code = models.IntegerField(verbose_name=_("status code"))
    content = models.TextField(verbose_name=_("content"))
    created = models.DateTimeField(
        verbose_name=_("created"),
        default=now,
        db_index=True,
        editable=False,
        blank=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="logresult_set",
    )
    view_token = models.UUIDField(verbose_name=_("view token"), default=uuid.uuid4, editable=False, blank=True, null=True)

    def __str__(self):
        return str(self.created)
