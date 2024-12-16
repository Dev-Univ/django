from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Project
from .services import ProjectService
from .serializers import ProjectRequestSerializer, ProjectResponseSerializer


class ProjectView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request):
        project_service = ProjectService(user=request.user)
        projects = project_service.get_projects()
        response_serializer = ProjectResponseSerializer(projects, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        request_serializer = ProjectRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        project_service = ProjectService(user=request.user)
        project = project_service.create_project(request_serializer.validated_data)

        response_serializer = ProjectResponseSerializer(project)
        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request, project_id):
        project_service = ProjectService(user=request.user)

        try:
            project = project_service.get_project(project_id)
            response_serializer = ProjectResponseSerializer(project)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)