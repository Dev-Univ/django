from django.urls import path

from univ.views import UnivView

urlpatterns = [
    path('<int:univ_id>', UnivView.as_view(), name='univ'),
]