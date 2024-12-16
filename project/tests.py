from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from PIL import Image
import io
import json

from user.models import User


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
        self.image_file = create_test_image()

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
                {"description": "Feature 1"},
                {"description": "Feature 2"}
            ],
            "additional_images": []
        }

        response = self.client.post(self.url, request, format='multipart')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], request['title'])
        self.assertEqual(response.data['short_description'], request['short_description'])
        self.assertEqual(response.data['description'], request['description'])
        self.assertIsNotNone(response.data['main_image_url'])
