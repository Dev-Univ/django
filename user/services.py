from django.db import transaction

from user.models import UserProfile


class UserService:

    def __init__(self, user, **kwargs):
        self.user = user

    @transaction.atomic
    def get_user_profile(self):
        # OnetoOne 관계라 objects 필요 없을 듯
        return self.user.profile

    @transaction.atomic
    def update_user_profile(self, profile_data):
        # 유저 프로필이 있으면 가져오고 없으면 생성
        profile, created = UserProfile.objects.get_or_create(user=self.user)

        # 프로필 데이터에서 key에 해당하는 속성이 있으면 value할당
        for key, value in profile_data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        # 데이터 유효성 검증
        profile.full_clean()
        profile.save()

        return profile
