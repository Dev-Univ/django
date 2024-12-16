from django.urls import path

from project.views import ProjectView, ProjectDetailView

urlpatterns = [
    path('', ProjectView.as_view(), name='project'),
    path('<int:project_id>', ProjectDetailView.as_view(), name='project-detail')
]