from django.urls import path, include
from notice.views import NoticeView, NoticeDetailView

urlpatterns = [
    path('', NoticeView.as_view(), name='notices'),
    path('<int:id>/', NoticeDetailView.as_view(), name='notice_detail'),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # CKEditor 업로드용
]
