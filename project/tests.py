from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from PIL import Image
import io

from project.models import Project, TechStack
from user.models import User

import json

def create_test_image():
    # 100x100 크기의 RGB 이미지 생성
    image = Image.new('RGB', (100, 100), color='red')

    # 이미지를 바이트로 변환
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)

    return SimpleUploadedFile(
        name='test_image.jpg',
        content=image_io.getvalue(),
        content_type='image/jpeg'
    )


class ProjectTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # 생성 유저
        self.user = User.objects.create_user(
            email="test@naver.com", name="tester", password="password"
        )
        # 프로젝트 멤버 유저
        self.user2 = User.objects.create_user(
            email="test2@naver.com", name="tester2", password="password"
        )
        self.image_file = create_test_image()
        self.tech_stack1 = TechStack.objects.create(
            title="Python",
            category="SERVER",
            sub_category="BACKEND"
        )
        self.tech_stack2 = TechStack.objects.create(
            title="React",
            category="CLIENT",
            sub_category="WEB_FRONTEND"
        )
        self.project = Project.objects.create(
            title="Test Project",
            is_done=False,
            short_description="Short test description",
            description="Detailed test description",
            main_image_url="https://test-bucket.s3.amazonaws.com/test.jpg",
            user=self.user
        )
        self.project2 = Project.objects.create(
            title="Test Project",
            is_done=False,
            short_description="Short test description",
            description="Detailed test description",
            main_image_url="https://test-bucket.s3.amazonaws.com/test.jpg",
            user=self.user
        )

    def test_post_project_success(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("project")

        request = {
            "title": "Test Project",
            "is_done": False,
            "short_description": "Short test description",
            "description": "Detailed test description",
            "main_image": self.image_file,
            "features": [
                "Feature 1",
                "Feature 2"
            ],
            "tech_stacks": [
                self.tech_stack1.id,
                self.tech_stack2.id
            ],
            "additional_images": [],
            "members": [
                self.user2.email
            ],
            "time_lines": json.dumps([
                {
                    "date": "2020-10-19",
                    "title": "Project Start",
                    "description": "Initial project planning phase"
                },
                {
                    "date": "2020-10-20",
                    "title": "Phase 1",
                    "description": "Development phase 1 completion"
                }
            ])
        }

        response = self.client.post(self.url, request, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], request['title'])
        self.assertEqual(response.data['short_description'], request['short_description'])
        self.assertEqual(response.data['description'], request['description'])
        self.assertIsNotNone(response.data['main_image_url'])
        self.assertEqual(len(response.data['tech_stacks']), 2)
        self.assertEqual(len(response.data['members']), 2)
        self.assertEqual(len(response.data['time_lines']), 2)

    def test_get_project_detail_success(self):
        url = reverse("project-detail", args=[self.project.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.project.title)

    def test_get_project_detail_not_found(self):
        url = reverse("project-detail", args=[9999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_projects_list_success(self):
        url = reverse("project")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        first_project = response.data[0]
        self.assertIn('title', first_project)
        self.assertIn('features', first_project)
        self.assertIn('additional_images', first_project)

    def test_get_projects_list_empty(self):
        # 기존 프로젝트 삭제
        Project.objects.all().delete()

        url = reverse("project")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
