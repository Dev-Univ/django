# # exceptions.py
# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.exceptions import ValidationError as DRFValidationError
# from django.core.exceptions import ValidationError as DjangoValidationError
# from django.db import DatabaseError, IntegrityError
#
#
# def custom_exception_handler(exc, context):
#     # 기본 DRF exception handler를 먼저 호출
#     response = exception_handler(exc, context)
#
#     # DRF ValidationError는 이미 처리되어 response가 있지만,
#     # 응답 형식을 우리가 원하는 형태로 변경
#     if isinstance(exc, DRFValidationError):
#         errors = []
#         for field, error_list in exc.detail.items():
#             errors.append(f"{field}: {error_list[0]}")
#
#         return Response(
#             {
#                 'error': '입력값이 유효하지 않습니다.',
#                 'details': errors
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     # 이미 처리된 다른 예외라면 그대로 반환
#     if response is not None:
#         return response
#
#     # Django ValidationError
#     if isinstance(exc, DjangoValidationError):
#         return Response(
#             {
#                 'error': '입력하신 데이터가 유효하지 않습니다.',
#                 'details': str(exc)
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     elif isinstance(exc, IntegrityError):
#         return Response(
#             {'error': '데이터 무결성 오류가 발생했습니다.'},
#             status=status.HTTP_409_CONFLICT
#         )
#
#     elif isinstance(exc, DatabaseError):
#         return Response(
#             {'error': '데이터베이스 오류가 발생했습니다.'},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
#
#     # 처리되지 않은 예외
#     return Response(
#         {'error': '서버 오류가 발생했습니다.'},
#         status=status.HTTP_500_INTERNAL_SERVER_ERROR
#     )