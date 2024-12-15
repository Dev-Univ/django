from django.urls import path

from univ.views import UnivView, UnivListView

urlpatterns = [
    # 모든 대학 정보 조회
    path('', UnivListView.as_view(), name='univ-list'),
    # 특정 대학 정보 아이디로 조회
    path('<int:univ_id>', UnivView.as_view(), name='univ'),
]