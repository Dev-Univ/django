from django.urls import path, include
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenVerifyView

from user.views import KakaoLoginView, KakaoCallbackView, UserProfileView, UserView

urlpatterns = [
    # dj-rest-auth URLs
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    path('auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('auth/registration/', RegisterView.as_view(), name='rest_register'),

    # 소셜 로그인 URLs
    path('kakao/login/', KakaoLoginView.as_view(), name='kakao-login'),
    path('kakao/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),

    # 사용자
    path('', UserView.as_view(), name='user'),
    # 사용자 프로필
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]