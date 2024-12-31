import uuid

import boto3
from botocore.exceptions import ClientError
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Prefetch

import univ
from devu import settings
from project.models import ProjectImage, Project, ProjectFeature, TechStack, ProjectTechStack, ProjectMember, TimeLine, \
    ProjectUniv
from univ.models import Univ
from .choices import ProjectMemberRole

User = get_user_model()


class ProjectService:
    def __init__(self, user):
        self.user = user
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

    @transaction.atomic
    def create_project(self, validated_data):
        try:
            print(validated_data)
            project = self._create_project_with_main_image(validated_data)
            self._create_additional_images(project, validated_data.get('additional_images', []))
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
        return Project.objects.prefetch_related(
            'features',
            'tech_stacks__tech_stack',
            'additional_images'
        ).get(id=project_id)

    @transaction.atomic
    def get_projects(self):
        return Project.objects.prefetch_related(
            'features',
            'tech_stacks__tech_stack',
            'additional_images',
            Prefetch('members', queryset=ProjectMember.objects.select_related(
                'user',
                'user__profile'
            )),
            'time_lines'
        ).order_by('-created_at')

    def _create_project_with_main_image(self, data):
        main_image_url = self.upload_image_to_s3(data['main_image'], "projects/main")
        return Project.objects.create(
            title=data['title'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            status=data['status'],
            short_description=data['short_description'],
            description=data['description'],
            main_image_url=main_image_url,
            user=self.user
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

        existing_tech_stacks = TechStack.objects.filter(id__in=tech_stacks_data)

        project_tech_stacks = [
            ProjectTechStack(
                project=project,
                tech_stack=tech_stack
            ) for tech_stack in existing_tech_stacks
        ]

        ProjectTechStack.objects.bulk_create(project_tech_stacks)

    def _create_univ(self, project, univ_data):
        if not univ_data:
            return

        existing_univ = Univ.objects.filter(id__in=univ_data)

        project_univ = [
            ProjectUniv(
                project=project,
                univ=univ
            ) for univ in existing_univ
        ]

        ProjectUniv.objects.bulk_create(project_univ)

    def _create_additional_images(self, project, images):
        if not images:
            return

        additional_images = [
            ProjectImage(
                project=project,
                image_url=self.upload_image_to_s3(image, "projects/additional")
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

    def upload_image_to_s3(self, image, folder: str = "projects") -> str:
        try:
            ext = image.name.split('.')[-1]
            file_path = f"{folder}/{self.user.id}/{uuid.uuid4()}.{ext}"

            self.s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                file_path,
            )

            return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_path}"

        except ClientError as e:
            raise Exception(f"Failed to upload image to S3: {str(e)}")
