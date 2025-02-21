from django.urls import path, include
from notice.views import NoticeView, NoticeDetailView

urlpatterns = [
    path('', NoticeView.as_view(), name='notices'),
    path('<int:id>/', NoticeDetailView.as_view(), name='notice_detail'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]
