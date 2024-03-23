from drf_yasg.utils import swagger_auto_schema
from mung_manager.common.base.serializers import BaseResponseSerializer, BaseSerializer
from mung_manager.common.exception.exceptions import NotFoundException
from mung_manager.common.mixins import APIAuthMixin
from mung_manager.common.response import create_response
from mung_manager.pet_kindergardens.enums import TicketType
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)
from mung_manager.pet_kindergardens.selectors.tickets import TicketSelector
from mung_manager.pet_kindergardens.services.tickets import TicketService
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class PetKindergardenTicketListView(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        usage_time_count = serializers.IntegerField()
        usage_count = serializers.IntegerField()
        usage_period_in_days_count = serializers.IntegerField()
        price = serializers.IntegerField()
        ticket_type = serializers.CharField()
        is_deleted = serializers.BooleanField()

    @swagger_auto_schema(
        tags=["반려동물 유치원"],
        operation_summary="반려동물 유치원 티켓 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def get(self, request: Request, pet_kindergarden_id: int) -> Response:
        """
        유저가 반려동물 유치원 티켓을 조회합니다.
        url: /partner/api/v1/pet-kindergardens/<int:pet_kindergarden_id>/tickets

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디

        Returns:
            OutSerializer: 반려동물 유치원 티켓 정보
                id (int): 티켓 아이디
                usage_time_count (int): 사용 시간 횟수
                usage_count (int): 사용 횟수
                usage_period_in_days_count (int): 사용 기간(일) 횟수
                price (int): 금액
                ticket_type (str): 티켓 타입
                is_deleted (bool): 삭제 여부
        """
        # 반려동물 유치원이 존재하는지 검증
        pet_kindergarden_selector = PetKindergardenSelector()

        if (
            pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarten_id=pet_kindergarden_id, user=request.user
            )
            is False
        ):
            raise NotFoundException(detail="PetKindergarden does not exist.", code="not_found_pet_kindergarden")

        # 티켓 조회
        ticket_selector = TicketSelector()
        tickets = ticket_selector.get_ticket_queryset_by_pet_kindergarden_id(pet_kindergarden_id=pet_kindergarden_id)
        tickets_data = self.OutputSerializer(tickets, many=True).data
        return create_response(data=tickets_data, status_code=status.HTTP_200_OK)

    class InputSerializer(BaseSerializer):
        usage_time_count = serializers.IntegerField(required=False, min_value=0, default=0)
        usage_count = serializers.IntegerField(required=True, min_value=1)
        usage_period_in_days_count = serializers.IntegerField(required=True, min_value=1)
        price = serializers.IntegerField(required=True, min_value=0)
        ticket_type = serializers.ChoiceField(choices=[type.value for type in TicketType])

    @swagger_auto_schema(
        tags=["반려동물 유치원"],
        operation_summary="반려동물 유치원 티켓 생성",
        request_body=InputSerializer,
        responses={
            status.HTTP_201_CREATED: BaseResponseSerializer(data_serializer=OutputSerializer),
        },
    )
    def post(self, request: Request, pet_kindergarden_id: int) -> Response:
        """
        유저가 반려동물 유치원 티켓을 생성합니다.
        url: /partner/api/v1/pet-kindergardens/<int:pet_kindergarden_id>/tickets

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            InputSerializer: 반려동물 유치원 티켓 생성 데이터
                usage_time_count (int): 사용 시간 횟수
                usage_count (int): 사용 횟수
                usage_period_in_days_count (int): 사용 기간(일) 횟수
                price (int): 금액
                ticket_type (str): 티켓 타입

        Returns:
            OutSerializer: 반려동물 유치원 티켓 정보
                id (int): 티켓 아이디
                usage_time_count (int): 사용 시간 횟수
                usage_count (int): 사용 횟수
                usage_period_in_days_count (int): 사용 기간(일)
                price (int): 금액
                ticket_type (str): 티켓 타입
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        # 반려동물 유치원이 존재하는지 검증
        pet_kindergarden_selector = PetKindergardenSelector()
        if (
            pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarten_id=pet_kindergarden_id,
                user=request.user,
            )
            is False
        ):
            raise NotFoundException(detail="PetKindergarden does not exist.", code="not_found_pet_kindergarden")

        # 티켓 생성
        ticket_service = TicketService()
        ticket = ticket_service.create_ticket(pet_kindergarden_id=pet_kindergarden_id, **input_serializer.validated_data)
        ticket_data = self.OutputSerializer(ticket).data
        return create_response(data=ticket_data, status_code=status.HTTP_201_CREATED)


class PetKindergardenTicketDetailView(APIAuthMixin, APIView):
    @swagger_auto_schema(
        tags=["반려동물 유치원"],
        operation_summary="반려동물 유치원 티켓 삭제",
        responses={
            status.HTTP_204_NO_CONTENT: "",
        },
    )
    def delete(self, request: Request, pet_kindergarden_id: int, ticket_id: int) -> Response:
        """
        유저가 반려동물 유치원 티켓을 삭제합니다.
        url: /partner/api/v1/pet-kindergardens/<int:pet_kindergarden_id>/tickets/<int:ticket_id>

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            ticket_id (int): 티켓 아이디
        """
        ticket_service = TicketService()
        ticket_service.delete_ticket(ticket_id=ticket_id, pet_kindergarden_id=pet_kindergarden_id, user=request.user)
        return create_response(status_code=status.HTTP_204_NO_CONTENT)
