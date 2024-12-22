from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from notice.models import Notice
from project.services import User


class NoticeTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@naver.com", name="tester", password="password"
        )
        self.notice = Notice.objects.create(
            title="test",
            category="GENERAL",
            content="test",
            is_pinned=False,
            is_active=True,
            author=self.user,
        )

    def test_retrieve_notices(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("notices")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.notice.id)
        self.assertEqual(response.data[0]["title"], self.notice.title)
        self.assertEqual(response.data[0]["category"], self.notice.category)
