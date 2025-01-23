from django.db import models

from univ.choices import Region


class Univ(models.Model):
    name = models.CharField(max_length=100)
    # todo: default, banlk 삭제
    code = models.CharField(max_length=50, default='', blank=True)
    description = models.TextField(max_length=500)
    region = models.CharField(max_length=100, choices=Region.choices)

    # todo: 학생, 프로젝트, 공지사항 fk로 연결
