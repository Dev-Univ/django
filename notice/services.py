from django.db import transaction
from django.db.models import Q

from notice.models import Notice


class NoticeService:
    @transaction.atomic
    def get_notices(self, search_query=None, category=None):
        queryset = Notice.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        if category and category != '전체':
            queryset = queryset.filter(category=category)

        return queryset.order_by('-created_at')

    @transaction.atomic
    def get_notice(self, id):
        return Notice.objects.get(id=id)
