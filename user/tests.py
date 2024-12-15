from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from user.models import UserProfile

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
        self.url = reverse("user-profile")
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
        self.url = reverse("user-profile")
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


class GetUserProfileTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # 요청 유저
        self.user = User.objects.create(
            email="test@naver.com", name="tester", password="password"
        )
        # profile 없는 유저 테스트
        self.user2 = User.objects.create(
            email="test2@naver.com", name="tester2", password="password2"
        )
        self.UserProfile = UserProfile.objects.create(
            user=self.user,
            school="서울대학교",
            major="컴퓨터공학과",
            self_introduction="테스트 자기소개",
            github_url="www.github.com/YunJae00",
            is_profile_private=True
        )

    # 유저 프로필 조회
    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("user-profile")
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 유저 프로필 생성 전 조회
    def test_get_user_profile_not_found(self):
        self.client.force_authenticate(user=self.user2)
        self.url = reverse("user-profile")
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


