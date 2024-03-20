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

    def check_is_exists_user_by_email_excluding_self(self, email: str, user) -> bool:
        """
        이 함수는 이메일로 자신을 제외한 유저를 조회합니다.

        Args:
            email (str): 이메일입니다.
            user (User): 유저 객체입니다.

        Returns:
            bool: 유저 존재 여부입니다.
        """
        return User.objects.filter(email=email).exclude(id=user.id).exists()
