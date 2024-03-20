from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from mung_manager.common.base.serializers import BaseResponseSerializer, BaseSerializer
from mung_manager.common.mixins import APIAuthMixin
from mung_manager.common.response import create_response
from mung_manager.files.enums import FileResourceType
from mung_manager.files.services import FileUploadService
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class FileUploadAPI(APIAuthMixin, APIView):
    parser_classes = (MultiPartParser,)

    class OutputSerializer(BaseSerializer):
        file_url = serializers.URLField()

    @swagger_auto_schema(
        tags=["파일"],
        operation_summary="파일 업로드",
        manual_parameters=[
            openapi.Parameter("file", openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
            openapi.Parameter(
                "resource_type", openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, enum=[e.value for e in FileResourceType]
            ),
        ],
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request) -> Response:
        """
        유저가 AWS S3에 파일을 업로드합니다. (최대 10MB)
        url: /partner/api/v1/files/upload

        Args:
            file (File): 업로드할 파일
            resource_type (str): 파일의 리소스 타입
        Returns:
            OutputSerializer:
                file_url: 업로드된 파일의 URL
        """
        file_service = FileUploadService(
            file_obj=request.FILES["file"],
            resource_type=request.data["resource_type"],
            user_id=request.user.id,
        )
        file_url = file_service.upload_file()
        file_data = self.OutputSerializer({"file_url": file_url}).data
        return create_response(file_data, status_code=status.HTTP_200_OK)
