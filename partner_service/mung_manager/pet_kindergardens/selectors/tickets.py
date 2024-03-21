from typing import Optional

from django.db.models.query import QuerySet
from mung_manager.pet_kindergardens.models import Ticket
from mung_manager.pet_kindergardens.selectors.abstracts import AbstractTicketSelector


class TicketSelector(AbstractTicketSelector):
    """
    이 클래스는 티켓을 SELECT, EXISTS를 위한 클래스입니다.
    """

    def get_ticket_queryset_by_pet_kindergarden_id(self, pet_kindergarden_id: int) -> QuerySet[Ticket]:
        """
        이 함수는 반려동물 유치원 아이디로 티켓 쿼리셋을 조회합니다.

        Args:
            pet_kindergarden_id: 반려동물 유치원 아이디입니다.

        Returns:
            QuerySet: 티켓 쿼리셋
        """
        return Ticket.objects.filter(pet_kindergarden_id=pet_kindergarden_id)

    def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """
        이 함수는 티켓 아이디로 티켓을 조회합니다.

        Args:
            ticket_id: 티켓 아이디입니다.

        Returns:
            Optional[Ticket]: 티켓 객체
        """
        try:
            return Ticket.objects.filter(id=ticket_id).get()

        except Ticket.DoesNotExist:
            return None
