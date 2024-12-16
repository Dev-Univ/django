from django.contrib.postgres.fields import ArrayField
from django.db import models

from user.models import User
from .choices import ProjectMemberRole


class Project(models.Model):
    title = models.CharField(max_length=100)
    is_done = models.BooleanField(default=False)
    short_description = models.TextField()
    description = models.TextField()
    main_image_url = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProjectFeature(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='features', on_delete=models.CASCADE)


class ProjectImage(models.Model):
    image_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, related_name='additional_images', on_delete=models.CASCADE)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ProjectMemberRole.choices, default=ProjectMemberRole.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

