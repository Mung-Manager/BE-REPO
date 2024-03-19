from drf_yasg.utils import swagger_auto_schema
from mung_manager.common.base.serializers import BaseResponseSerializer, BaseSerializer
from mung_manager.common.mixins import APIAuthMixin
from mung_manager.common.response import create_response
from mung_manager.users.services.users import UserService
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserProfileView(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        name = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.CharField()

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 상세 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        """
        유저가 자신의 정보를 상세 조회합니다.
        url: /partner/api/v1/users/profile

        Returns:
            OutSerializer: 유저 정보
                name (str): 이름
                email (str): 이메일
                phone_number (str): 전화번호
        """
        user_data = self.OutputSerializer(request.user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)

    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True, max_length=32)
        email = serializers.EmailField(required=True, max_length=256)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 수정",
        request_body=InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def patch(self, request: Request) -> Response:
        """
        유저가 자신의 정보를 수정합니다.
        url: /partner/api/v1/users/profile

        Args:
            name (str): 이름
            email (str): 이메일

        Returns:
            OutSerializer: 유저 정보
                name (str): 이름
                email (str): 이메일
                phone_number (str): 전화번호
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user_service = UserService()
        user = user_service.update_user(user=request.user, data=input_serializer.validated_data)
        user_data = self.OutputSerializer(user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)
