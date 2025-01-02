from django.db.models import Sum
from django.utils import timezone

from theme.models import Theme


class ThemeService:

    def get_current_theme(self):
        today = timezone.now().date()
        theme = Theme.objects.prefetch_related('teams', 'teams__positions').get(
            start_date__lte=today,
            end_date__gte=today
        )

        theme.team_count = theme.teams.count()
        theme.total_positions = theme.teams.aggregate(
            total=Sum('positions__current_members'))['total'] or 0

        return theme
