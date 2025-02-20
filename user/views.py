from django.conf import settings
import requests
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserProfileRequestSerializer, UserSerializer, \
    PrivateUserProfileResponseSerializer, PublicUserProfileResponseSerializer, UserSetUpRequestSerializer
from .services import UserService
from urllib.parse import urlencode

User = get_user_model()


class UserProfileView(GenericAPIView):
    serializer_class = UserSerializer

    @permission_classes([AllowAny])
    def get(self, request, email):
        userService = UserService()

        try:
            token = request.auth
            user = userService.get_user_by_email(email)

            # 자신의 프로필 조회
            if token and email == token.payload['email']:
                response_serializer = PrivateUserProfileResponseSerializer(user)
            # 다른 유저가 프로필 조회
            else:
                response_serializer = PublicUserProfileResponseSerializer(user)

            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @permission_classes([IsAuthenticated])
    def post(self, request, email):
        userService = UserService()

        request_serializer = UserProfileRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        # 유저 프로필 업데이트 (만약 처음이라면 생성)
        user = userService.update_user_profile(request_serializer.validated_data, request.user)
        response_serializer = PrivateUserProfileResponseSerializer(user)

        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class UserSetUpView(GenericAPIView):

    @permission_classes([IsAuthenticated])
    def post(self, request):
        request_serializer = UserSetUpRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        user = request.user
        data = request_serializer.validated_data

        if data['selected_profile'] == 'custom':
            user.name = data['name']
            user.profile_image_url = ''

        user.is_initial_profile_set = True
        user.save()

        return Response(status=status.HTTP_200_OK)


class KakaoLoginView(APIView):
    def get(self, request):
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = settings.KAKAO_CONFIG['KAKAO_REDIRECT_URI']

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'profile_nickname account_email profile_image',
            'prompt': 'select_account',
        }

        kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?{urlencode(params)}"
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
        refresh['email'] = user.email  # 이메일 추가

        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # 프론트엔드로 리다이렉트 (토큰과 함께)
        redirect_uri = f"http://localhost:3000/login/kakao-callback?access={tokens['access']}&refresh={tokens['refresh']}&email={user.email}&name={user.name}&profile_image_url={user.profile_image_url}&is_initial_profile_set={user.is_initial_profile_set}"
        return redirect(redirect_uri)

    def get_kakao_token(self, code):
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = settings.KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        client_secret = settings.KAKAO_CONFIG['KAKAO_CLIENT_SECRET']

        token_url = "https://kauth.kakao.com/oauth/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'code': code,
            'client_secret': client_secret,
        }

        response = requests.post(token_url, data=data, headers=headers)
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
            user.social_profile_name = str(kakao_account.get('profile', {}).get('nickname', '')),
            if user.profile_image_url != '':
                user.profile_image_url = str(kakao_account.get('profile', {}).get('thumbnail_image_url', ''))
            user.save()
        except User.DoesNotExist:
            # 새로운 사용자 생성
            user = User.objects.create_user(
                email=email,
                name=kakao_account.get('profile', {}).get('nickname', ''),
                social_profile_name=kakao_account.get('profile', {}).get('nickname', ''),
                kakao_id=str(user_info.get('id')),
                profile_image_url=kakao_account.get('profile', {}).get('thumbnail_image_url', ''),
                is_initial_profile_set=False
            )

        return user


class UserWithdrawalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, email):
        # 본인 계정만 탈퇴 가능하도록 체크
        if email != request.user.email:
            return Response(
                {"detail": "You can only withdraw your own account."},
                status=status.HTTP_403_FORBIDDEN
            )

        userService = UserService()

        try:
            userService.withdraw_user(request.user)
            return Response(
                {"detail": "Account successfully deleted."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": "Failed to withdraw account."},
                status=status.HTTP_400_BAD_REQUEST
            )