from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class UserProfileUpdateCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # 생성 유저
        self.user = User.objects.create(
            email="test@naver.com", name="tester", password="password"
        )

    def test_user_profile_update(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("update-user-profile")
        request = {
            "school": "서울대학교",
            "major": "컴퓨터공학과",
            "self_introduction": "자기소개 예시입니다.",
            "github_url": "www.github.com/YunJae00"
        }
        response = self.client.post(self.url, request, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_update_validation_fail(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("update-user-profile")
        request = {
            "school": "서울대학교" * 100,
            "major": "컴퓨터공학과",
            "self_introduction": "자기소개 예시입니다.",
            "github_url": "www.github.com/YunJae00"
        }
        response = self.client.post(self.url, request, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], '입력값이 유효하지 않습니다.')
        self.assertIn('school', str(response.data['details']))
