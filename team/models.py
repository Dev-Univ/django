from django.db import models

from project.models import TechStack
from theme.models import Theme
from user.models import User
from .choices import Subject


class Team(models.Model):
    name = models.CharField(max_length=100)
    # todo: 이거 default 랑 blank 다 삭제해야함
    type = models.CharField(choices=Subject.choices, max_length=100)
    period = models.CharField(max_length=100, default='', blank=True)
    short_description = models.TextField(default='', blank=True)
    description = models.TextField()
    collaboration_method = models.TextField(default='', blank=True)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, related_name='teams')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')


class TeamTechStack(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tech_stacks')
    tech_stack = models.ForeignKey(TechStack, on_delete=models.CASCADE)


class Position(models.Model):
    role = models.CharField(max_length=100)
    max_members = models.PositiveIntegerField(default=1)
    current_members = models.PositiveIntegerField(default=0)
    description = models.TextField()
    is_open = models.BooleanField(default=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='positions')