from django.urls import path

from team.views import TeamView, TeamDetailView, TeamListView

urlpatterns = [
    path('', TeamView.as_view(), name='team'),
    path('<int:team_id>/', TeamDetailView.as_view(), name='team_detail'),
    path('my-teams/', TeamListView.as_view(), name='my-teams'),
]