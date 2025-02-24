from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, Q, F, FloatField, Max, Case, When, Value
from django.db.models.functions import Cast, Power

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
            'students': User.objects.filter(profile__school__isnull=False).exclude(profile__school='').count()
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
        # 프로젝트 상태별 가중치
        status_weights = {
            'PLANNING': 0.3,      # 계획중
            'IN_PROGRESS': 0.6,   # 진행중
            'COMPLETED': 1.0,     # 완료
            'SUSPENDED': 0.2,     # 중단
        }

        univ_scores = Univ.objects.annotate(
            # 프로젝트 통계
            total_projects=Count('projectuniv__project', distinct=True),
            planning_projects=Count(
                'projectuniv__project',
                filter=Q(projectuniv__project__status='PLANNING'),
                distinct=True
            ),
            in_progress_projects=Count(
                'projectuniv__project',
                filter=Q(projectuniv__project__status='IN_PROGRESS'),
                distinct=True
            ),
            completed_projects=Count(
                'projectuniv__project',
                filter=Q(projectuniv__project__status='COMPLETED'),
                distinct=True
            ),
            suspended_projects=Count(
                'projectuniv__project',
                filter=Q(projectuniv__project__status='SUSPENDED'),
                distinct=True
            ),

            # 프로젝트 품질 관련 평균값
            avg_features=Case(
                When(total_projects__gt=0,
                     then=Cast(Count('projectuniv__project__features') * 1.0 / F('total_projects'), FloatField())),
                default=Value(0.0, output_field=FloatField())
            ),
            avg_tech_stacks=Case(
                When(total_projects__gt=0,
                     then=Cast(Count('projectuniv__project__tech_stacks') * 1.0 / F('total_projects'), FloatField())),
                default=Value(0.0, output_field=FloatField())
            ),
            avg_time_lines=Case(
                When(total_projects__gt=0,
                     then=Cast(Count('projectuniv__project__time_lines') * 1.0 / F('total_projects'), FloatField())),
                default=Value(0.0, output_field=FloatField())
            ),
            avg_team_size=Case(
                When(total_projects__gt=0,
                     then=Cast(Count('projectuniv__project__members') * 1.0 / F('total_projects'), FloatField())),
                default=Value(0.0, output_field=FloatField())
            ),
            unique_tech_categories=Count(
                'projectuniv__project__tech_stacks__tech_stack__category',
                distinct=True
            ),
        ).annotate(
            # 프로젝트 점수: 프로젝트 수에 따라 자연스럽게 증가 (0.6 제곱근 사용)
            project_score=Case(
                When(total_projects__gt=0,
                     then=Cast(300 * Power(F('total_projects'), 0.6), FloatField())),
                default=Value(0.0, output_field=FloatField())
            ),

            # 진행도 점수: 실제 진행 상태의 가중 평균
            completion_score=Case(
                When(total_projects__gt=0,
                     then=Cast(
                         500 * (
                                 F('planning_projects') * status_weights['PLANNING'] +
                                 F('in_progress_projects') * status_weights['IN_PROGRESS'] +
                                 F('completed_projects') * status_weights['COMPLETED'] +
                                 F('suspended_projects') * status_weights['SUSPENDED']
                         ) / F('total_projects'),
                         FloatField()
                     )),
                default=Value(0.0, output_field=FloatField())
            ),

            # 품질 점수: 실제 구현된 것들의 평균으로 계산
            quality_score=Case(
                When(total_projects__gt=0,
                     then=Cast(
                         300 * (
                                 F('avg_features') + F('avg_tech_stacks') + F('avg_time_lines') +
                                 Cast(F('avg_team_size'), FloatField()) / 5.0 +
                                 Cast(F('unique_tech_categories'), FloatField()) / 3.0
                         ) / 7.0,
                         FloatField()
                     )),
                default=Value(0.0, output_field=FloatField())
            )
        ).annotate(
            total_score=F('project_score') + F('completion_score') + F('quality_score')
        ).filter(
            total_score__gt=0
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
                'project_score': round(univ.project_score, 2),
                'completion_score': round(univ.completion_score, 2),
                'quality_score': round(univ.quality_score, 2),
                'completed_ratio': round(univ.completed_projects * 100 / univ.total_projects if univ.total_projects > 0 else 0, 2),
                'avg_features': round(univ.avg_features, 2),
                'avg_tech_stacks': round(univ.avg_tech_stacks, 2)
            }
        } for idx, univ in enumerate(univ_scores)]

    def _get_max_value(self, field):
        if field == 'total_projects':
            max_count = Univ.objects.annotate(
                count=Count('projectuniv__project')
            ).aggregate(max_count=Max('count'))['max_count']
            return max_count if max_count else 1
        return 1
