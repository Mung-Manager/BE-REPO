from abc import ABC, abstractmethod
from typing import Optional

from mung_manager.users.models import User


class AbstractUserSelector(ABC):
    @abstractmethod
    def get_user_by_social_id(self, social_id: str) -> Optional[User]:
        pass
