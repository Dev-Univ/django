from django.db import models
from django.utils import timezone

from user.models import User
from .choices import ProjectMemberRole, TechStackCategoryChoices


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
    role = models.CharField(max_length=100, choices=ProjectMemberRole.choices, default=ProjectMemberRole.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')


class TechStack(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=TechStackCategoryChoices.choices)
    sub_category = models.CharField(max_length=100, choices=TechStackCategoryChoices.choices)


class ProjectTechStack(models.Model):
    project = models.ForeignKey(Project, related_name='tech_stacks', on_delete=models.CASCADE)
    tech_stack = models.ForeignKey(TechStack, related_name='projects', on_delete=models.CASCADE)


class UserTechStack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tech_stack = models.ForeignKey(TechStack, related_name='users', on_delete=models.CASCADE)


class TimeLine(models.Model):
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='time_lines', on_delete=models.CASCADE)