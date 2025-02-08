from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from univ.models import Univ
from univ.serializers import UnivResponseSerializer, UnivInfoResponseSerializer, UnivRankingResponseSerializer
from univ.services import UnivService


class UnivView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        univService = UnivService()

        univs = univService.get_all_univs()
        serializer = UnivResponseSerializer(univs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UnivDetailView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, univ_id):
        univService = UnivService()

        try:
            univ = univService.get_univ(univ_id)
            serializer = UnivResponseSerializer(univ)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UnivInfoView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        univService = UnivService()

        try:
            univ_info = univService.get_univ_info()
            serializer = UnivInfoResponseSerializer(univ_info)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UnivRankingView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        대학 랭킹 조회
        - region: 지역별 필터링
        - limit: 상위 N개 대학 필터링
        """
        univService = UnivService()

        try:
            rankings = univService.get_univ_rankings()

            # 필터링 적용
            rankings = self._apply_filters(rankings, request.query_params)

            response_data = {
                'rankings': rankings,
                'total_count': len(rankings)
            }

            serializer = UnivRankingResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # def post(self, request, *args, **kwargs):
    #     """
    #     랭킹 캐시 갱신 (관리자 전용)
    #     """
    #     univService = UnivService()
    #
    #     if not request.user.is_staff:
    #         return Response(
    #             {'error': 'Permission denied'},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #
    #     try:
    #         cache.delete('university_rankings')
    #         rankings = univService.get_univ_rankings()
    #         return Response(
    #             {'message': 'Rankings refreshed successfully'},
    #             status=status.HTTP_200_OK
    #         )
    #     except Exception as e:
    #         return Response(
    #             {'error': str(e)},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

    def _apply_filters(self, rankings, query_params):
        """필터링 로직 적용"""
        filtered_rankings = rankings

        # 지역 필터
        region = query_params.get('region')
        if region:
            filtered_rankings = [
                r for r in filtered_rankings
                if r['region'] == region
            ]

        # 상위 N개 필터
        limit = query_params.get('limit')
        if limit:
            try:
                limit = int(limit)
                filtered_rankings = filtered_rankings[:limit]
            except ValueError:
                pass

        return filtered_rankings


