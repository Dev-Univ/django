from django.conf import settings
from django.contrib.sites import requests
from django.shortcuts import redirect
from rest_framework import status, request
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserProfileRequestSerializer, UserProfileResponseSerializer
from .services import UserService

User = get_user_model()


class UpdateUserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserProfileRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userService = UserService(user=request.user)

        # 유저 프로필 업데이트 (만약 처음이라면 생성)
        updated_profile = userService.update_user_profile(serializer.validated_data)
        response_serializer = UserProfileResponseSerializer(updated_profile)

        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


# todo: 나중에 kakao login 도 Serializer 만들어야함
class KakaoLoginView(APIView):
    def get(self, request):
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = settings.KAKAO_CONFIG['KAKAO_REDIRECT_URI']

        kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

        return Response({'auth_url': kakao_auth_url})


class KakaoCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({'error': 'Authentication code not provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 액세스 토큰 받기
        token_response = self.get_kakao_token(code)
        if not token_response.get('access_token'):
            return Response({'error': 'Failed to get access token'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 카카오 사용자 정보 받기
        user_info = self.get_kakao_user_info(token_response.get('access_token'))
        if not user_info:
            return Response({'error': 'Failed to get user info'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 사용자 생성 또는 로그인 처리
        user = self.get_or_create_user(user_info)

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # 프론트엔드로 리다이렉트 (토큰과 함께)
        redirect_uri = f"http://localhost:3000/login/kakao-callback?access={tokens['access']}&refresh={tokens['refresh']}"
        return redirect(redirect_uri)

    def get_kakao_token(self, code):
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = settings.KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        client_secret = settings.KAKAO_CONFIG['KAKAO_CLIENT_SECRET']

        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'code': code,
            'client_secret': client_secret,
        }

        response = requests.post(token_url, data=data)
        return response.json()

    def get_kakao_user_info(self, access_token):
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }

        response = requests.get(user_info_url, headers=headers)
        return response.json()

    def get_or_create_user(self, user_info):
        kakao_account = user_info.get('kakao_account')
        if not kakao_account:
            raise ValueError('Failed to get kakao account info')

        email = kakao_account.get('email')
        if not email:
            raise ValueError('Email not provided')

        try:
            user = User.objects.get(email=email)
            # 기존 사용자의 카카오 정보 업데이트
            user.kakao_id = str(user_info.get('id'))
            user.save()
        except User.DoesNotExist:
            # 새로운 사용자 생성
            user = User.objects.create_user(
                email=email,
                name=kakao_account.get('profile', {}).get('nickname', ''),
                kakao_id=str(user_info.get('id'))
            )

        return user
