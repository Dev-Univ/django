import uuid

import boto3
from botocore.exceptions import ClientError
from django.db import transaction

from devu import settings
from project.models import ProjectImage, Project, ProjectFeature


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
            self._create_additional_images(project, validated_data.get('additional_images', []))

            return Project.objects.prefetch_related(
                'features',
                'additional_images'
            ).get(id=project.id)

        except Exception as e:
            raise Exception(f"Failed to create project: {str(e)}")

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
                description=feature_data['description']
            ) for feature_data in features_data
        ]
        ProjectFeature.objects.bulk_create(features)

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
