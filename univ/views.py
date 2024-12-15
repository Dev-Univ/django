from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from univ.models import Univ
from univ.serializers import UnivResponseSerializer
from univ.services import UnivService


class UnivView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, univ_id):
        univService = UnivService(user=request.user)

        try:
            univ = univService.get_univ(univ_id)
            serializer = UnivResponseSerializer(univ)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Univ.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UnivListView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        univService = UnivService(user=request.user)

        univs = univService.get_all_univs()
        serializer = UnivResponseSerializer(univs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

