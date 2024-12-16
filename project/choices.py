from django.db.models import TextChoices


class ProjectMemberRole(TextChoices):
    # 첫번째가 실제 저장 값, 두번째가 label
    LEADER = "LEADER", "팀장"
    MEMBER = "MEMBER", "팀원"
