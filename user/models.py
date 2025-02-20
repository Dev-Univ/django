from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    social_profile_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image_url = models.TextField(blank=True, null=True)

    is_initial_profile_set = models.BooleanField(default=False)

    # 인증 관련
    kakao_id = models.CharField(max_length=100, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    school_email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # 학교 정보
    school = models.CharField(max_length=100, blank=True, default='')
    major = models.CharField(max_length=100, blank=True, default='')

    # 프로필 정보
    self_introduction = models.TextField(blank=True, max_length=1000)
    github_url = models.TextField(blank=True, default='', max_length=255)
    is_profile_private = models.BooleanField(default=False)
