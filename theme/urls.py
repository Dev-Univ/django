from django.urls import path

from theme.views import ThemeView

urlpatterns = [
    path('', ThemeView.as_view(), name='theme'),
]