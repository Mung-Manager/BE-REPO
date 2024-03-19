from typing import Optional

from mung_manager.users.models import User
from mung_manager.users.selectors.abstracts import AbstractUserSelector


class UserSelector(AbstractUserSelector):
    """
    이 클래스는 유저를 SELECT, EXISTS를 위한 클래스입니다.
    """

    def get_user_by_social_id(self, social_id: str) -> Optional[User]:
        """
        이 함수는 소셜 아이디로 유저를 조회합니다.

        Args:
            social_id (str): 소셜 아이디입니다.

        Returns:
            Optional[User]: 유저 객체입니다.
        """
        try:
            return User.objects.filter(social_id=social_id).get()
        except User.DoesNotExist:
            return None
