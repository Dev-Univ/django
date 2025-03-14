from django.urls import path

from project.views import ProjectView, ProjectDetailView, ProjectListView, ProjectRelatedListView, UnivProjectListView

urlpatterns = [
    path('', ProjectView.as_view(), name='project'),
    path('<int:project_id>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<str:user_email>/', ProjectListView.as_view(), name='project-list'),
    path('univ/<int:univ_id>/', UnivProjectListView.as_view(), name='project-list'),
    path('related/<int:project_id>/', ProjectRelatedListView.as_view(), name='project-list-related')
]