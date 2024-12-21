from django.db.models import TextChoices


class Subject(TextChoices):
    # 첫번째가 실제 저장 값, 두번째가 label
    FREE_SUBJECET = "FREE_SUBJECET", "자유 주제"
    MONTHLY_SUBJECT = "MONTHLY_SUBJECT", "월간 주제"
