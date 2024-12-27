from django.contrib import admin

from project.models import Project, TechStack, UserTechStack

# Register your models here.
admin.site.register(Project)
admin.site.register(TechStack)
admin.site.register(UserTechStack)