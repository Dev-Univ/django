import uuid

import boto3
from botocore.exceptions import ClientError
from django.contrib.auth import get_user_model
from django.db import transaction

from devu import settings
from project.models import ProjectImage, Project, ProjectFeature, TechStack, ProjectTechStack, ProjectMember
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
            project = self._create_project_with_main_image(validated_data)
            self._create_features(project, validated_data.get('features', []))
            self._create_tech_stacks(project, validated_data.get('tech_stacks', []))
            self._create_additional_images(project, validated_data.get('additional_images', []))
            self._create_project_members(project, validated_data.get('members', []))

            # prefetch_related는 역참조할 때 주로 사용함
            return Project.objects.prefetch_related(
                'features',
                'tech_stacks__tech_stack',
                'additional_images',
                'members',
                'members__user',
                'members__user__profile'
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
            'additional_images'
        ).all()

    def _create_project_with_main_image(self, data):
        main_image_url = self.upload_image_to_s3(data['main_image'], "projects/main")
        return Project.objects.create(
            title=data['title'],
            is_done=data['is_done'],
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

    def _create_project_members(self, project, member_emails):
        if not member_emails:
            return

        members = User.objects.filter(email__in=member_emails)

        # 프로젝트 생성자를 OWNER로 추가
        ProjectMember.objects.create(
            project=project,
            user=self.user,
            role=ProjectMemberRole.LEADER
        )

        # 나머지 멤버들을 MEMBER로 추가
        project_members = [
            ProjectMember(
                project=project,
                user=member,
                role=ProjectMemberRole.MEMBER
            ) for member in members if member != self.user
        ]

        if project_members:
            ProjectMember.objects.bulk_create(project_members)

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
