from django.utils import timezone

from theme.models import Theme


class ThemeService:

    def get_current_theme(self):
        today = timezone.now().date()
        return Theme.objects.get(
            # (Less Than or Equal) (Greater Than or Equal)
            start_date__lte=today,
            end_date__gte=today
        )

