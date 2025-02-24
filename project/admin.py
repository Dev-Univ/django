from django.contrib import admin

from project.models import Project, TechStack, ProjectUniv, ProjectFeature, ProjectMember, ProjectImage, \
    ProjectTechStack, TimeLine

# Register your models here.
admin.site.register(Project)
admin.site.register(TechStack)
admin.site.register(ProjectUniv)
admin.site.register(ProjectFeature)
admin.site.register(ProjectImage)
admin.site.register(ProjectMember)
admin.site.register(ProjectTechStack)
admin.site.register(TimeLine)
