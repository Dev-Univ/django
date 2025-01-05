from django.db import models
from django.utils import timezone

from univ.models import Univ
from user.models import User
from .choices import ProjectMemberRole, TechStackCategoryChoices, TechStackSubCategoryChoices, ProjectStatus


class Project(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=ProjectStatus.choices, max_length=100, default=ProjectStatus.COMPLETED)
    short_description = models.TextField()
    description = models.TextField()
    main_image_url = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 이거는 프로젝트 생성 유저
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProjectUniv(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE)


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
    description = models.TextField(default='추후에 설명을 입력해주세요.')
    joined_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')


class TechStack(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=TechStackCategoryChoices.choices)
    sub_category = models.CharField(max_length=100, choices=TechStackSubCategoryChoices.choices)


class ProjectTechStack(models.Model):
    project = models.ForeignKey(Project, related_name='tech_stacks', on_delete=models.CASCADE)
    tech_stack = models.ForeignKey(TechStack, related_name='projects', on_delete=models.CASCADE)


class UserTechStack(models.Model):
    user = models.ForeignKey(User, related_name='tech_stacks', on_delete=models.CASCADE)
    tech_stack = models.ForeignKey(TechStack, related_name='users', on_delete=models.CASCADE)


class TimeLine(models.Model):
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=1)
    project = models.ForeignKey(Project, related_name='time_lines', on_delete=models.CASCADE)