from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from univ.models import Univ
from user.models import User


class UnivTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        # 생성 유저
        self.user = User.objects.create_user(
            email="test@naver.com", name="tester", password="password"
        )
        self.univ = Univ.objects.create(
            name="서울대학교", description="대학교 설명 예시", region="서울"
        )
        self.univ2 = Univ.objects.create(
            name="연세대학교", description="대학교 설명 예시", region="서울"
        )

    def test_get_univ(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("univ-detail", args=[self.univ.id])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.univ.name)

    def test_get_failure(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("univ-detail", args=[100])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_univs(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("univ")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
