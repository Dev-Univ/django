from django.contrib import admin

from project.models import UserTechStack
from .models import User, UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserTechStack)
