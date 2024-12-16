from django.urls import path

from project.views import ProjectView

urlpatterns = [
    path('', ProjectView.as_view(), name='project')
]