from django.utils import timezone
from mung_manager.common.exception.exceptions import AuthenticationFailedException
from mung_manager.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    """
    이 클래스는 인증과 관련된 비즈니스 로직을 담당합니다.
    """

    def generate_token(self, user: User) -> tuple[str, str]:
        """
        이 함수는 유저로 refresh_token과 access_token을 생성합니다.

        Args:
            user: 유저 객체입니다.

        Returns:
            Union[str, str]: refresh_token, access_token입니다.
        """
        refresh_token = RefreshToken.for_user(user)
        return str(refresh_token), str(refresh_token.access_token)

    def authenticate_user(self, user: User) -> User:
        """
        이 함수는 유저의 활성화 상태를 검증하고,
        마지막 로그인 시간 및 삭제 상태를 업데이트합니다.

        Args:
            user: 유저 객체입니다.

        Returns:
            User: 유저 객체입니다.
        """

        # 유저가 활성화 검증
        if user.is_active is False:
            raise AuthenticationFailedException("User is not active")

        # 유저가 삭제되었을 때, 삭제 상태를 업데이트
        if user.is_deleted is True and user.deleted_at is not None:
            user.is_deleted = False
            user.deleted_at = None

        # 마지막 로그인 시간을 업데이트
        user.last_login = timezone.now()
        user.save(update_fields=["is_deleted", "deleted_at", "last_login"])

        return user
