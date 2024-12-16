from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import ProjectService
from .serializers import ProjectRequestSerializer, ProjectResponseSerializer


class ProjectView(GenericAPIView):

    @permission_classes([IsAuthenticated])
    def post(self, request):
        request_serializer = ProjectRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        project_service = ProjectService(user=request.user)
        project = project_service.create_project(request_serializer.validated_data)

        response_serializer = ProjectResponseSerializer(project)
        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)