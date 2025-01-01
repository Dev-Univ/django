from django.db import models

from project.models import TechStack
from user.models import User
from .choices import Subject


class Team(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(choices=Subject.choices, max_length=100)
    description = models.TextField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')


class TeamTechStack(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tech_stacks')
    tech_stack = models.ForeignKey(TechStack, on_delete=models.CASCADE)


class Position(models.Model):
    role = models.CharField(max_length=100)
    quota = models.PositiveIntegerField(default=1)
    description = models.TextField()
    is_open = models.BooleanField(default=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='positions')