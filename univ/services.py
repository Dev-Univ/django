from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, Q, F, FloatField, Max, Case, When
from django.db.models.functions import Cast

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

    @transaction.atomic
    def get_univ_rankings(self):
        cache_key = 'university_rankings'
        rankings = cache.get(cache_key)

        if rankings is None:
            rankings = self._calculate_rankings()
            cache.set(cache_key, rankings, 60 * 60)  # 1시간 캐시

        return rankings

    def _calculate_rankings(self):
        weights = {
            'project_count': 0.3,
            'completed_ratio': 0.2,
            'project_quality': 0.2,
            'student_participation': 0.3,
        }

        univ_scores = Univ.objects.annotate(
            total_projects=Count('projectuniv__project', distinct=True),
            completed_projects=Count(
                'projectuniv__project',
                filter=Q(projectuniv__project__status='COMPLETED'),
                distinct=True
            ),
            completed_ratio=Case(
                When(total_projects__gt=0,
                     then=Cast(F('completed_projects') * 100.0 / F('total_projects'), FloatField())),
                default=0.0
            ),
            avg_features=Case(
                When(total_projects__gt=0,
                     then=Cast(Count('projectuniv__project__features') * 1.0 / F('total_projects'), FloatField())),
                default=0.0
            ),
            avg_timelines=Case(
                When(total_projects__gt=0,
                     then=Cast(Count('projectuniv__project__time_lines') * 1.0 / F('total_projects'), FloatField())),
                default=0.0
            ),
            avg_tech_stacks=Case(
                When(total_projects__gt=0,
                     then=Cast(Count('projectuniv__project__tech_stacks') * 1.0 / F('total_projects'), FloatField())),
                default=0.0
            ),
        ).annotate(
            project_score=Case(
                When(total_projects__gt=0,
                     then=F('total_projects') * 1.0 / self._get_max_value('total_projects') * weights['project_count']),
                default=0.0
            ),
            completion_score=F('completed_ratio') / 100.0 * weights['completed_ratio'],
            quality_score=Case(
                When(total_projects__gt=0,
                     then=((F('avg_features') + F('avg_timelines') + F('avg_tech_stacks')) / 3.0) * weights['project_quality']),
                default=0.0
            ),
        ).annotate(
            total_score=F('project_score') + F('completion_score') + F('quality_score')
        ).order_by('-total_score')

        return [{
            'rank': idx + 1,
            'id': univ.id,
            'name': univ.name,
            'region': univ.region,
            'total_score': round(univ.total_score, 2),
            'details': {
                'project_count': univ.total_projects,
                'completed_projects': univ.completed_projects,
                'project_score': univ.project_score,
                'completion_score': univ.completion_score,
                'quality_score': univ.quality_score,
                'completed_ratio': round(univ.completed_ratio, 1),
                'avg_features': round(univ.avg_features, 1),
                'avg_tech_stacks': round(univ.avg_tech_stacks, 1)
            }
        } for idx, univ in enumerate(univ_scores)]

    def _get_max_value(self, field):
        if field == 'total_projects':
            max_count = Univ.objects.annotate(
                count=Count('projectuniv__project')
            ).aggregate(max_count=Max('count'))['max_count']
            return max_count if max_count else 1
        return 1
