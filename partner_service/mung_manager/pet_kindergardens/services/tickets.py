from django.db import transaction
from django.utils import timezone
from mung_manager.common.exception.exceptions import NotFoundException
from mung_manager.common.services import update_model
from mung_manager.pet_kindergardens.models import Ticket
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)
from mung_manager.pet_kindergardens.selectors.tickets import TicketSelector


class TicketService:
    """
    이 클래스는 티켓과 관련된 비즈니스 로직을 담당합니다.
    """

    def __init__(self):
        self.ticket_selector = TicketSelector()
        self.pet_kindergarden_selector = PetKindergardenSelector()

    @transaction.atomic
    def create_ticket(
        self,
        pet_kindergarden_id: int,
        usage_time: int,
        usage_count: int,
        usage_period_in_days: int,
        price: int,
        ticket_type: str,
    ) -> Ticket:
        """
        이 함수는 티켓 데이터를 받아 티켓을 생성합니다.

        Args:
            pet_kindergarden_id: 반려동물 유치원 아이디입니다.
            usage_time: 사용시간입니다.
            usage_count: 사용횟수입니다.
            usage_period_in_days: 사용기간입니다.
            price: 가격입니다.
            ticket_type: 티켓 타입입니다.

        Returns:
            Ticket: 티켓 객체입니다.
        """
        ticket = Ticket(
            pet_kindergarden_id=pet_kindergarden_id,
            usage_time=usage_time,
            usage_count=usage_count,
            usage_period_in_days=usage_period_in_days,
            price=price,
            ticket_type=ticket_type,
            deleted_at=None,
        )

        # 티켓 데이터 검증 후 저장
        ticket.full_clean()
        ticket.save()

        return ticket

    @transaction.atomic
    def delete_ticket(self, ticket_id: int, pet_kindergarden_id: int, user) -> Ticket:
        """
        이 함수는 티켓의 삭제 여부를 True로 변경합니다.

        Args:
            ticket_id: 티켓 아이디입니다.
            pet_kindergarden_id: 반려동물 유치원 아이디입니다.
            user: 유저 객체입니다.

        Returns:
            Ticket: 티켓 객체입니다.
        """
        if (
            self.pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarten_id=pet_kindergarden_id,
                user=user,
            )
            is False
        ):
            raise NotFoundException(detail="PetKindergarden does not exist.", code="not_found_pet_kindergarden")

        # 티켓이 존재하는지 검증
        ticket = self.ticket_selector.get_ticket_by_id(ticket_id)

        if ticket is None:
            raise NotFoundException(detail="Ticket does not exist.", code="not_found_ticket")

        # 티켓 삭제 여부 변경
        if ticket.is_deleted is False and ticket.deleted_at is None:
            fields = ["is_deleted", "deleted_at"]
            data = {"is_deleted": True, "deleted_at": timezone.now()}
            ticket, has_updated = update_model(instance=ticket, fields=fields, data=data)

        return ticket
