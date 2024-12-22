import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from project.models import TechStack
from team.models import Team, Position
from user.models import User


class TeamTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # 생성 유저
        self.user = User.objects.create_user(
            email="test@naver.com", name="tester", password="password"
        )
        self.user2 = User.objects.create_user(
            email="test2@naver.com", name="tester2", password="password"
        )
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
        self.team = Team.objects.create(
            name="Team 1",
            description="Team description",
            end_date="2020-10-20",
            user=self.user
        )
        self.team2 = Team.objects.create(
            name="Team 2",
            description="Team description",
            end_date="2020-10-20",
            user=self.user2
        )
        self.position = Position.objects.create(
            name="Position 1",
            description="Position description",
            is_open=False,
            team=self.team
        )

    def test_post_team_success(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("team")

        request = {
            "name": "Test Team",
            "type": "MONTHLY_SUBJECT",
            "description": "Test Description",
            "end_date": "2025-01-01",
            "tech_stacks": [
                self.tech_stack1.id,
                self.tech_stack2.id
            ],
            "positions": [
                {
                    "name": "Test Position",
                    "description": "Test Description",
                    "is_open": True
                },
                {
                    "name": "Test Position2",
                    "description": "Test Description2",
                    "is_open": True
                },
            ]
        }

        response = self.client.post(self.url, json.dumps(request), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TechStack.objects.count(), 2)

    def test_post_team_missing_required_field_failure(self):
        # 필수 필드 누락 테스트
        self.client.force_authenticate(user=self.user)
        self.url = reverse("team")

        request = {
            "name": "Test Team",
            # type 필드 누락
            "description": "Test Description",
            "end_date": "2025-01-01",
            "positions": [
                {
                    "name": "Test Position",
                    "description": "Test Description",
                    "is_open": True
                }
            ]
        }

        response = self.client.post(self.url, json.dumps(request), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)

    def test_post_team_invalid_date_format_failure(self):
        # 잘못된 날짜 형식 테스트
        self.client.force_authenticate(user=self.user)
        self.url = reverse("team")

        request = {
            "name": "Test Team",
            "type": "MONTHLY_SUBJECT",
            "description": "Test Description",
            "end_date": "2025/01/01",  # 잘못된 날짜 형식
            "positions": [
                {
                    "name": "Test Position",
                    "description": "Test Description",
                    "is_open": True
                }
            ]
        }

        response = self.client.post(self.url, json.dumps(request), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('end_date', response.data)

    def test_post_team_invalid_position_data_failure(self):
        # 잘못된 position 데이터 테스트
        self.client.force_authenticate(user=self.user)
        self.url = reverse("team")

        request = {
            "name": "Test Team",
            "type": "MONTHLY_SUBJECT",
            "description": "Test Description",
            "end_date": "2025-01-01",
            "positions": [
                {
                    "name": "Test Position",
                    # description 필드 누락
                    "is_open": True
                }
            ]
        }

        response = self.client.post(self.url, json.dumps(request), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('positions', response.data)


        # todo: 존재하지 않는 tech stack ID 테스트

    def test_retrieve_teams_success(self):
        self.client.force_authenticate(user=self.user)
        self.url = reverse("team")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_teams_by_user_success(self):
        self.client.force_authenticate(user=self.user2)
        self.url = reverse("my-teams")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
