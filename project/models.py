from django.db import models
from django.utils import timezone

from univ.models import Univ
from user.models import User
from .choices import ProjectMemberRole, TechStackCategoryChoices, TechStackSubCategoryChoices, ProjectStatus, \
    ProjectSaveForm


class Project(models.Model):
    title = models.CharField(max_length=100)
    form_mode = models.CharField(choices=ProjectSaveForm.choices, max_length=100, default=ProjectSaveForm.BASIC_FORM)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    status = models.CharField(choices=ProjectStatus.choices, max_length=100, default=ProjectStatus.COMPLETED)
    short_description = models.TextField()
    description = models.TextField()
    main_image_url = models.CharField(max_length=500, blank=True)
    read_me_content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 이거는 프로젝트 생성 유저
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ProjectUniv(models.Model):
    project = models.ForeignKey(Project, related_name='project_univs', on_delete=models.CASCADE)
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE)


class ProjectFeature(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='features', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project.title} - description: {self.description}'


class ProjectImage(models.Model):
    image_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, related_name='additional_images', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project.title} - image'


class ProjectMember(models.Model):
    role = models.CharField(max_length=100, choices=ProjectMemberRole.choices, default=ProjectMemberRole.MEMBER)
    description = models.TextField()
    joined_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return f'{self.project.title} - members'


class TechStack(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=TechStackCategoryChoices.choices)
    sub_category = models.CharField(max_length=100, choices=TechStackSubCategoryChoices.choices)

    def __str__(self):
        return self.title


class ProjectTechStack(models.Model):
    project = models.ForeignKey(Project, related_name='tech_stacks', on_delete=models.CASCADE)
    tech_stack = models.ForeignKey(TechStack, related_name='projects', on_delete=models.CASCADE)


class UserTechStack(models.Model):
    user = models.ForeignKey(User, related_name='tech_stacks', on_delete=models.CASCADE)
    tech_stack = models.ForeignKey(TechStack, related_name='users', on_delete=models.CASCADE)


class TimeLine(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=1)
    project = models.ForeignKey(Project, related_name='time_lines', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project.title} - timeline'
