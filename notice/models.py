from django.contrib.auth import get_user_model
from django.db import models

from notice.choices import NoticeCategory

User = get_user_model()


class Notice(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(choices=NoticeCategory.choices, max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)  # 상단 고정 여부
    is_active = models.BooleanField(default=True)  # 공개/비공개 여부
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
