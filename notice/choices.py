from django.db.models import TextChoices


class NoticeCategory(TextChoices):
    # 첫번째가 실제 저장 값, 두번째가 label
    GENERAL = 'general', '일반'
    URGENT = 'urgent', '긴급'
    EVENT = 'event', '이벤트'
    UPDATE = 'update', '업데이트'
    MAINTENANCE = 'maintenance', '점검'