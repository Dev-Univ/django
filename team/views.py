from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from team.serializers import TeamRequestSerializer, TeamResponseSerializer
from team.services import TeamService
from utils.paginations import CustomPagination


class TeamView(GenericAPIView):

    @permission_classes([AllowAny])
    def post(self, request):
        team_service = TeamService()

        request_serializer = TeamRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        team = team_service.create_team(request_serializer.validated_data, request.user)

        response_serializer = TeamResponseSerializer(team)

        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)

    @permission_classes([AllowAny])
    def get(self, request):
        team_service = TeamService()

        teams = team_service.get_teams()

        paginator = CustomPagination()
        paginated_teams = paginator.paginate_queryset(teams, request)

        response_serializer = TeamResponseSerializer(paginated_teams, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class TeamDetailView(GenericAPIView):

    @permission_classes([IsAuthenticated])
    def get(self, request):
        team_service = TeamService()

        team = team_service.get_teams_by_user(request.user)

        response_serializer = TeamResponseSerializer(team, many=True)

        return Response(data=response_serializer.data, status=status.HTTP_200_OK)