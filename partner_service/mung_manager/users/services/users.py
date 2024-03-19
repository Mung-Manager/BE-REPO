from collections import OrderedDict

from django.db import transaction
from mung_manager.common.services import update_model
from mung_manager.users.models import User
from mung_manager.users.selectors.users import UserSelector


class UserService:
    """
    이 클래스는 유저와 관련된 비즈니스 로직을 담당합니다.
    """

    def __init__(self):
        self.user_selector = UserSelector()

    @transaction.atomic
    def create_social_user(
        self,
        email: str,
        name: str,
        social_id: str,
        phone_number: str,
        birth: object,
        gender: str,
        social_provider: int,
    ) -> User:
        """
        이 함수는 유저 데이터를 받아 소셜 유저를 생성합니다.

        Args:
            email (str): 이메일입니다.
            name (str): 이름입니다.
            social_id (str): 소셜 아이디입니다.
            phone_number (str): 전화번호입니다.
            birth (Union[str, datetime, None]): 생년월일입니다.
            gender (Optional[str]): 성별입니다.
            social_provider (int): 소셜 제공자입니다.

        Returns:
            User: 유저 객체입니다.
        """
        # 소셜 아이디로 유저 조회
        user = self.user_selector.get_user_by_social_id(social_id)

        # 유저가 존재하지 않을 경우 생성
        if user is None:
            user = User.objects.create_social_user(
                email=email,
                name=name,
                phone_number=phone_number,
                social_id=social_id,
                social_provider=social_provider,
                birth=birth,
                gender=gender,
            )
        return user

    @transaction.atomic
    def update_user(self, user, data: OrderedDict) -> User:
        """
        이 함수는 유저 데이터를 받아 유저를 수정합니다.

        Args:
            user (User): 유저 객체입니다.
            data (dict): 수정할 데이터입니다.

        Returns:
            User: 유저 객체입니다.
        """
        # 유저 정보 수정
        fields = ["name", "email"]
        user, has_updated = update_model(instance=user, fields=fields, data=data)
        return user
