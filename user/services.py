from django.db import transaction

from project.models import UserTechStack, TechStack
from user.models import UserProfile, User


class UserService:

    @transaction.atomic
    def get_user_by_email(self, email):
        return User.objects.select_related(
            'profile',
        ).prefetch_related(
            'tech_stacks'
        ).get(email=email)

    @transaction.atomic
    def update_user_profile(self, profile_data, user):
        tech_stack_codes = profile_data.pop('tech_stacks', [])

        # 유저 프로필이 있으면 가져오고 없으면 생성
        profile, created = UserProfile.objects.get_or_create(user=user)

        # 프로필 데이터에서 key에 해당하는 속성이 있으면 value할당
        for key, value in profile_data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        # 데이터 유효성 검증
        profile.full_clean()
        profile.save()

        # 기존 tech stack 관계 모두 삭제
        UserTechStack.objects.filter(user=user).delete()

        # 새로운 tech stack 관계 생성
        tech_stacks_to_create = []
        for tech_stack_code in tech_stack_codes:
            try:
                tech_stack = TechStack.objects.get(code=tech_stack_code)
                tech_stacks_to_create.append(
                    UserTechStack(user=user, tech_stack=tech_stack)
                )
            except TechStack.DoesNotExist:
                continue

        if tech_stacks_to_create:
            UserTechStack.objects.bulk_create(tech_stacks_to_create)

        return User.objects.select_related(
            'profile',
        ).prefetch_related(
            'tech_stacks'
        ).get(id=user.id)
