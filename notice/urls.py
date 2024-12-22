from django.urls import path

from notice.views import NoticeView

urlpatterns = [
    path('', NoticeView.as_view(), name='notices'),
]