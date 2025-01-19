from django.urls import path

from univ.views import UnivView, UnivDetailView

urlpatterns = [
    # 모든 대학 정보 조회
    path('', UnivView.as_view(), name='univ'),
    # 특정 대학 정보 아이디로 조회
    path('<int:univ_id>/', UnivDetailView.as_view(), name='univ-detail'),
]