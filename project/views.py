from datetime import datetime

from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

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

            # 조회수 증가 로직 구현
            # 클라이언트 IP 가져오기
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR')

            # 캐시 유효 시간을 1시간으로 설정하고 캐시 키에는 시간 정보를 포함하지 않음
            cache_key = f'project_view_{project_id}_{ip_address}'
            cache.set(cache_key, True, 60 * 60)  # 1시간(3600초) 유지

            # 캐시에서 조회 기록 확인
            viewed = cache.get(cache_key)

            # 해당 시간에 처음 조회하는 경우에만 조회수 증가
            if not viewed:
                project.views += 1
                project.save(update_fields=['views'])

                # 조회 기록 캐싱 (1시간 유지)
                cache.set(cache_key, True, 60 * 60)  # 1시간 유지

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

    @permission_classes([IsAuthenticated])
    def delete(self, request, project_id):
        project_service = ProjectService()

        try:
            project_service.delete_project(project_id, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_403_FORBIDDEN
                if 'Permission denied' in str(e)
                else status.HTTP_400_BAD_REQUEST
            )


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
    def get(self, request, univ_id):
        project_service = ProjectService()

        projects = project_service.get_projects_by_univ_code(univ_id)

        response_serializer = ProjectListSerializer(projects, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class ProjectRelatedListView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request, project_id):
        project_service = ProjectService()

        projects = project_service.get_related_projects(project_id)

        response_serializer = ProjectListSerializer(projects, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)