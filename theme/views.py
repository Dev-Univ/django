from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from theme.models import Theme
from theme.serializers import ThemeResponseSerializer
from theme.services import ThemeService


class ThemeView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request):
        theme_service = ThemeService()

        try:
            theme = theme_service.get_current_theme()
            response_serializer = ThemeResponseSerializer(theme)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except Theme.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
