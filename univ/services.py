from django.db import transaction
from django.db.models import Count, Q, F

from project.models import ProjectUniv, Project
from univ.models import Univ
from user.models import User, UserProfile


class UnivService:

    @transaction.atomic
    def get_univ(self, univ_id):
        return Univ.objects.filter(id=univ_id).annotate(
            student_count=Count(
                'id',
                filter=Q(code__in=UserProfile.objects.values('school')),
                distinct=True
            ),
            project_count=Count(
                'projectuniv__project',
                distinct=True
            )
        ).values(
            'id',
            'name',
            'description',
            'region',
            'student_count',
            'project_count'
        ).first()

    @transaction.atomic
    def get_all_univs(self):
        return Univ.objects.all()

    @transaction.atomic
    def get_univ_info(self):
        total_info = {
            'univs': Univ.objects.filter(
                id__in=ProjectUniv.objects.values('univ_id').distinct()
            ).count(),
            'projects': Project.objects.select_related('user').count(),
            'students': User.objects.filter().count(),
        }

        universities = list(Univ.objects.filter(
            id__in=ProjectUniv.objects.values('univ_id').distinct()
        ).annotate(
            student_count=Count(
                'id',
                filter=Q(code__in=UserProfile.objects.values('school')),
                distinct=True
            ),
            project_count=Count(
                'projectuniv__project',
                distinct=True
            )
        ).values(
            'id',
            'name',
            'description',
            'region',
            'student_count',
            'project_count'
        ))

        return {
            'total_info': total_info,
            'universities': universities
        }
