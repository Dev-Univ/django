from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from utils.paginations import CustomPagination
from .models import Project
from .services import ProjectService
from .serializers import ProjectRequestSerializer, ProjectResponseSerializer, ProjectListSerializer


class ProjectView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request):
        project_service = ProjectService()
        search_query = request.query_params.get('search', '')

        projects = project_service.get_projects(search_query)
        paginator = CustomPagination()
        paginated_projects = paginator.paginate_queryset(projects, request)

        response_serializer = ProjectListSerializer(paginated_projects, many=True)
        return Response(
            data=paginator.get_paginated_response(response_serializer.data),
            status=status.HTTP_200_OK
        )

    @permission_classes([IsAuthenticated])
    def post(self, request):
        project_service = ProjectService()

        request_serializer = ProjectRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        project = project_service.create_project(request_serializer.validated_data, request.user)

        response_serializer = ProjectResponseSerializer(project)
        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request, project_id):
        project_service = ProjectService()

        try:
            project = project_service.get_project(project_id)
            response_serializer = ProjectResponseSerializer(
                project,
                context={'request': request}
            )
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @permission_classes([IsAuthenticated])
    def put(self, request, project_id):
        project_service = ProjectService()

        request_serializer = ProjectRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        project = project_service.update_project(project_id, request_serializer.validated_data, request.user)

        response_serializer = ProjectResponseSerializer(project)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


# todo: 나중에 쿼리 파라미터로 통합하기
class ProjectListView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request, user_email):
        project_service = ProjectService()

        projects = project_service.get_projects_by_user_email(user_email)

        response_serializer = ProjectListSerializer(projects, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class UnivProjectListView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request, univ_code):
        project_service = ProjectService()

        projects = project_service.get_projects_by_univ_code(univ_code)

        response_serializer = ProjectListSerializer(projects, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class ProjectRelatedListView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request, project_id):
        project_service = ProjectService()

        projects = project_service.get_related_projects(project_id)

        response_serializer = ProjectListSerializer(projects, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)