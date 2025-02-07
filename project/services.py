import json
import uuid

import boto3
from botocore.exceptions import ClientError
from django.contrib.auth import get_user_model
from django.db import transaction

import univ
from devu import settings
from project.models import ProjectImage, Project, ProjectFeature, TechStack, ProjectTechStack, ProjectMember, TimeLine, \
    ProjectUniv
from univ.models import Univ
from .choices import ProjectMemberRole

from django.db.models import Q

User = get_user_model()


class ProjectService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

    @transaction.atomic
    def create_project(self, validated_data, user):
        try:
            project = self._create_project_with_main_image(validated_data, user)
            self._create_additional_images(project, validated_data.get('additional_images', []), user)
            self._create_features(project, validated_data.get('features', []))
            self._create_tech_stacks(project, validated_data.get('tech_stacks', []))
            self._create_univ(project, validated_data.get('univ', []))
            self._create_project_members(project, validated_data.get('members', []))
            self._create_time_line(project, validated_data.get('time_lines', []))

            # prefetch_related는 역참조할 때 주로 사용함
            return Project.objects.prefetch_related(
                'features',
                'tech_stacks__tech_stack',
                'additional_images',
                'members',
                'members__user',
                'members__user__profile',
                'time_lines'
            ).get(id=project.id)

        except Exception as e:
            raise Exception(f"Failed to create project: {str(e)}")

    @transaction.atomic
    def get_project(self, project_id):
        return (Project.objects.prefetch_related(
            'features',
            'tech_stacks__tech_stack',
            'additional_images',
            'project_univs__univ',
            'members__user__profile',
            'time_lines'
        ).select_related('user').get(id=project_id))

    @transaction.atomic
    def get_projects(self, search_query=None):
        queryset = Project.objects.prefetch_related(
            'tech_stacks__tech_stack',
        ).select_related('user')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(tech_stacks__tech_stack__title__icontains=search_query)
            ).distinct()

        return queryset.order_by('-created_at')

    @transaction.atomic
    def update_project(self, project_id, validated_data, user):
        try:
            project = Project.objects.get(id=project_id)

            if project.user != user:
                raise Exception("Permission denied: You are not the owner of this project")

            # 메인 이미지와 기본 필드들 한번에 업데이트
            update_fields = []
            if 'main_image' in validated_data:
                project.main_image_url = self.upload_image_to_s3(validated_data['main_image'], user, "projects/main")
                update_fields.append('main_image_url')

            basic_fields = [
                'title', 'form_mode', 'start_date', 'end_date', 'status',
                'short_description', 'description', 'read_me_content'
            ]
            for field in basic_fields:
                if field in validated_data:
                    setattr(project, field, validated_data[field])
                    update_fields.append(field)

            if update_fields:
                project.save(update_fields=update_fields)

            # 각 related 필드들은 bulk operation으로 한번에 처리
            if 'additional_images' in validated_data:
                ProjectImage.objects.filter(project=project).delete()
                if validated_data['additional_images']:
                    ProjectImage.objects.bulk_create([
                        ProjectImage(
                            project=project,
                            image_url=self.upload_image_to_s3(image, user, "projects/additional")
                        ) for image in validated_data['additional_images']
                    ])

            if 'features' in validated_data:
                ProjectFeature.objects.filter(project=project).delete()
                if validated_data['features']:
                    ProjectFeature.objects.bulk_create([
                        ProjectFeature(project=project, description=feature)
                        for feature in validated_data['features']
                    ])

            if 'tech_stacks' in validated_data:
                ProjectTechStack.objects.filter(project=project).delete()
                if validated_data['tech_stacks']:
                    tech_stacks = TechStack.objects.filter(code__in=validated_data['tech_stacks'])
                    ProjectTechStack.objects.bulk_create([
                        ProjectTechStack(project=project, tech_stack=tech_stack)
                        for tech_stack in tech_stacks
                    ])

            if 'univ' in validated_data:
                ProjectUniv.objects.filter(project=project).delete()
                if validated_data['univ']:
                    univs = Univ.objects.filter(code__in=validated_data['univ'])
                    ProjectUniv.objects.bulk_create([
                        ProjectUniv(project=project, univ=univ)
                        for univ in univs
                    ])

            if 'members' in validated_data:
                members_data = (
                    json.loads(validated_data['members'])
                    if isinstance(validated_data['members'], str)
                    else validated_data['members']
                )
                if members_data:
                    ProjectMember.objects.filter(project=project).delete()
                    emails = [member['user_email'] for member in members_data]
                    users = {
                        user.email: user
                        for user in User.objects.filter(email__in=emails)
                    }
                    ProjectMember.objects.bulk_create([
                        ProjectMember(
                            project=project,
                            user=users[member['user_email']],
                            role=member['role'],
                            description=member.get('description', '')
                        ) for member in members_data
                        if member['user_email'] in users
                    ])

            if 'time_lines' in validated_data:
                TimeLine.objects.filter(project=project).delete()
                if validated_data['time_lines']:
                    TimeLine.objects.bulk_create([
                        TimeLine(
                            project=project,
                            date=timeline['date'],
                            title=timeline['title'],
                            description=timeline['description'],
                            order=timeline['order']
                        ) for timeline in validated_data['time_lines']
                    ])

            return Project.objects.prefetch_related(
                'features',
                'tech_stacks__tech_stack',
                'additional_images',
                'members',
                'members__user',
                'members__user__profile',
                'time_lines'
            ).get(id=project.id)

        except Project.DoesNotExist:
            raise Exception("Project not found")
        except Exception as e:
            raise Exception(f"Failed to update project: {str(e)}")

    @transaction.atomic
    def get_projects_by_user_email(self, user_email):
        return Project.objects.filter(user__email=user_email).prefetch_related(
            'tech_stacks__tech_stack',
        ).select_related('user').order_by('-created_at')

    def _create_project_with_main_image(self, data, user):
        main_image_url = (
            self.upload_image_to_s3(data['main_image'], user, "projects/main")
            if data.get('main_image')
            else ''
        )
        return Project.objects.create(
            title=data['title'],
            form_mode=data['form_mode'],
            start_date=data.get('start_date', None),
            end_date=data.get('end_date', None),
            status=data['status'],
            short_description=data['short_description'],
            description=data['description'],
            read_me_content=data.get('read_me_content', ''),
            main_image_url=main_image_url,
            user=user
        )

    def _create_features(self, project, features_data):
        if not features_data:
            return

        features = [
            ProjectFeature(
                project=project,
                description=feature_data
            ) for feature_data in features_data
        ]
        ProjectFeature.objects.bulk_create(features)

    def _create_tech_stacks(self, project, tech_stacks_data):
        if not tech_stacks_data:
            return

        try:
            # tech_stacks_data가 리스트인지 확인
            if not isinstance(tech_stacks_data, list):
                tech_stacks_data = [tech_stacks_data]

            existing_tech_stacks = TechStack.objects.filter(code__in=tech_stacks_data)

            if not existing_tech_stacks.exists():
                return  # 또는 에러 처리

            project_tech_stacks = [
                ProjectTechStack(
                    project=project,
                    tech_stack=tech_stack
                ) for tech_stack in existing_tech_stacks
            ]

            ProjectTechStack.objects.bulk_create(project_tech_stacks)

        except Exception as e:
            raise Exception(f"Failed to create tech stacks: {str(e)}")

    def _create_univ(self, project, univ_data):
        if not univ_data:
            return

        existing_univ = Univ.objects.filter(code__in=univ_data)

        project_univ = [
            ProjectUniv(
                project=project,
                univ=univ
            ) for univ in existing_univ
        ]

        ProjectUniv.objects.bulk_create(project_univ)

    def _create_additional_images(self, project, images, user):
        if not images:
            return

        additional_images = [
            ProjectImage(
                project=project,
                image_url=self.upload_image_to_s3(image, user, "projects/additional")
            ) for image in images
        ]
        ProjectImage.objects.bulk_create(additional_images)

    def _create_project_members(self, project, members_data):
        if not members_data:
            return

        try:
            print(members_data)
            # members_data가 이미 dict 리스트인지 확인
            if isinstance(members_data, str):
                import json
                members_data = json.loads(members_data)

            # members_data는 [{'role': 'LEADER', 'user_email': 'test@test.com', 'description': '설명'}, ...] 형태
            email_to_role = {member['user_email']: member['role'] for member in members_data}
            email_to_description = {member['user_email']: member.get('description', '') for member in members_data}
            emails = list(email_to_role.keys())

            # 이메일로 유저들 조회
            members = User.objects.filter(email__in=emails)

            # 각 유저별로 해당하는 role 적용
            project_members = [
                ProjectMember(
                    project=project,
                    user=member,
                    role=email_to_role[member.email],
                    description=email_to_description[member.email]
                ) for member in members
            ]

            if project_members:
                ProjectMember.objects.bulk_create(project_members)
        except Exception as e:
            raise Exception(f"Failed to create project members: {str(e)}")

    def _create_time_line(self, project, timelines_data):
        if not timelines_data:
            return

        timelines = [
            TimeLine(
                project=project,
                date=timeline['date'],
                title=timeline['title'],
                description=timeline['description'],
                order=timeline['order']
            ) for timeline in timelines_data
        ]

        TimeLine.objects.bulk_create(timelines)

    def upload_image_to_s3(self, image, user, folder: str = "projects") -> str:
        try:
            ext = image.name.split('.')[-1]
            file_path = f"{folder}/{user.id}/{uuid.uuid4()}.{ext}"

            self.s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                file_path,
            )

            return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_path}"

        except ClientError as e:
            raise Exception(f"Failed to upload image to S3: {str(e)}")
