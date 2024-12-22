from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from notice.serializers import NoticeResponseSerializer
from notice.services import NoticeService


class NoticeView(GenericAPIView):

    @permission_classes([AllowAny])
    def get(self, request):
        notice_service = NoticeService()

        notices = notice_service.get_all_notices()

        response_serializer = NoticeResponseSerializer(notices, many=True)

        return Response(data=response_serializer.data, status=status.HTTP_200_OK)
