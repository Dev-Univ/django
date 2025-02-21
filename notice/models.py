from django.contrib.auth import get_user_model
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from notice.choices import NoticeCategory

User = get_user_model()


class Notice(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(choices=NoticeCategory.choices, max_length=255)
    content = CKEditor5Field()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
