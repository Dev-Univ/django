from django.urls import path

from project.views import ProjectView, ProjectDetailView, ProjectListView, ProjectRelatedListView

urlpatterns = [
    path('', ProjectView.as_view(), name='project'),
    path('<int:project_id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<str:user_email>/', ProjectListView.as_view(), name='project-list'),
    path('related/<int:project_id>/', ProjectRelatedListView.as_view(), name='project-list-related')
]