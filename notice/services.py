from django.db import transaction

from notice.models import Notice


class NoticeService:

    @transaction.atomic
    def get_all_notices(self):
        return Notice.objects.all()
