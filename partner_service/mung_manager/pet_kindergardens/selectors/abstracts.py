from abc import ABC, abstractmethod
from typing import Optional

from django.db.models.query import QuerySet
from mung_manager.pet_kindergardens.models import (
    PetKindergarden,
    RawPetKindergarden,
    Ticket,
)


class AbstractPetKindergardenSelector(ABC):
    @abstractmethod
    def check_is_exists_pet_kindergarden_by_user(self, user) -> bool:
        pass

    @abstractmethod
    def get_pet_kindergarden_by_id_and_user(self, pet_kindergarten_id: int, user) -> Optional[PetKindergarden]:
        pass

    @abstractmethod
    def check_is_exists_pet_kindergarden_by_id_and_user(self, pet_kindergarten_id: int, user) -> bool:
        pass


class AbstractRawPetKindergardenSelector(ABC):
    @abstractmethod
    def get_raw_pet_kindergarden_queryset_by_name(self, name: str) -> QuerySet[RawPetKindergarden]:
        pass


class AbstractTicketSelector(ABC):
    @abstractmethod
    def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        pass

    @abstractmethod
    def get_ticket_queryset_by_pet_kindergarden_id(self, pet_kindergarden_id: int) -> QuerySet[Ticket]:
        pass
