from django.urls import path

from notice.views import NoticeView, NoticeDetailView

urlpatterns = [
    path('', NoticeView.as_view(), name='notices'),
    path('<int:id>/', NoticeDetailView.as_view(), name='notice_detail',)
]