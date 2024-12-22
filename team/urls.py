from django.urls import path

from team.views import TeamView, TeamDetailView

urlpatterns = [
    path('', TeamView.as_view(), name='team'),
    path('my-teams/', TeamDetailView.as_view(), name='my-teams'),
]