"""
Django settings for devu project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os
import json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# CORS 설정
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

AUTH_USER_MODEL = "user.User"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'corsheaders',
    'boto3',
    # custom apps
    "user",
    "univ",
    "project",
    "theme",
    "team",
    "notice",
]

MIDDLEWARE = [
    # allauth middleware
    'allauth.account.middleware.AccountMiddleware',
    # cors
    'corsheaders.middleware.CorsMiddleware',
    # django 기본
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'devu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# all-auth
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# kakao OAuth 설정
KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": get_secret("KAKAO_REST_API_KEY"),
    "KAKAO_REDIRECT_URI": get_secret("KAKAO_REDIRECT_URI"),
    "KAKAO_CLIENT_SECRET": get_secret("KAKAO_CLIENT_SECRET"),
}

# DRF, Simple-JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "PAGE_SIZE": 10,  # DEFAULT_PAGE_SIZE 대신 직접 숫자 지정
    "DEFAULT_PAGINATION_CLASS": "utils.paginations.CustomPagination",
    # 'EXCEPTION_HANDLER': 'devu.exceptions.custom_exception_handler'
}

# JWT 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),    # 액세스 토큰 30분
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),       # 리프레시 토큰 1일
    'ROTATE_REFRESH_TOKENS': True,                     # 리프레시 토큰 재발급
    'BLACKLIST_AFTER_ROTATION': True,                  # 사용된 리프레시 토큰 블랙리스트
    'UPDATE_LAST_LOGIN': True,                         # 마지막 로그인 시간 업데이트
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),                  # Bearer 인증 방식
    'TOKEN_OBTAIN_SERIALIZER': 'users.serializers.CustomTokenObtainPairSerializer', # claim 커스터마이징
}

# dj-rest-auth 설정
REST_USE_JWT = True  # JWT 사용 설정
JWT_AUTH_COOKIE = 'access_token'  # 액세스 토큰을 저장할 쿠키 이름
JWT_AUTH_REFRESH_COOKIE = 'refresh_token'  # 리프레시 토큰을 저장할 쿠키 이름


ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 이메일로 로그인
ACCOUNT_EMAIL_REQUIRED = True           # 이메일 필드 필수
ACCOUNT_UNIQUE_EMAIL = True             # 이메일 중복 불가
ACCOUNT_USERNAME_REQUIRED = False        # username 필드 불필요
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # username 필드 사용 안함

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': get_secret("KAKAO_REST_API_KEY"),
            'secret': get_secret("KAKAO_CLIENT_SECRET"),
            'key': ''
        },
        'SCOPE': [
            'profile_nickname',    # 카카오에서 가져올 정보: 닉네임
            # 'account_email',       # 카카오에서 가져올 정보: 이메일
        ],
        # 'PROFILE_FIELDS': [       # 실제로 가져올 필드 지정
        #     'nickname',
        #     'email',
        # ],
    }
}

SOCIALACCOUNT_AUTO_SIGNUP = True          # 소셜 로그인 시 자동 회원가입
# SOCIALACCOUNT_EMAIL_REQUIRED = True        # 소셜 계정에서도 이메일 필수
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'  # 소셜 계정 이메일 인증 불필요

# s3
AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'devu-project-images'
AWS_S3_REGION_NAME = 'ap-northeast-2'
