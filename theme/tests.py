from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from theme.models import Theme


class ThemeTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.current_date = datetime.now()
        self.theme = Theme.objects.create(
            title="December Projects",
            short_description="December Projects",
            description="Build something for the holidays",
            month=self.current_date.month,
            year=self.current_date.year,
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now()
        )
        self.url = reverse('theme')

    def test_get_current_month_theme_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.theme.title)
        self.assertEqual(response.data['month'], self.current_date.month)
        self.assertEqual(response.data['year'], self.current_date.year)
