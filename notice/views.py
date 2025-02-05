from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from notice.serializers import NoticeResponseSerializer
from notice.services import NoticeService
from utils.paginations import CustomPagination


class NoticeView(GenericAPIView):
    @permission_classes([AllowAny])
    def get(self, request):
        notice_service = NoticeService()
        search_query = request.query_params.get('search', '')
        category = request.query_params.get('category', '')

        notices = notice_service.get_notices(search_query, category)
        paginator = CustomPagination()
        paginated_notices = paginator.paginate_queryset(notices, request)

        response_serializer = NoticeResponseSerializer(paginated_notices, many=True)

        return Response(
            data=paginator.get_paginated_response(response_serializer.data),
            status=status.HTTP_200_OK
        )
