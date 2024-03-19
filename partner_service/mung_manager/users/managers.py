from django.contrib.auth.models import BaseUserManager
from mung_manager.users.enums import AuthGroup, UserProvider


class UserManager(BaseUserManager):
    def create_social_user(self, email: str, social_id: str, social_provider: int, **extra_fields):
        """
        이 함수는 유저 데이터를 받아 소셜 유저를 생성합니다.

        Args:
            email (str): 이메일입니다.
            social_id (str): 소셜 아이디입니다.
            social_provider (int): 소셜 제공자입니다.
            **extra_fields: 추가적인 필드입니다.

        Returns:
            User: 유저 객체입니다.
        """
        email = self.normalize_email(email)
        user = self.model(
            social_id=social_id,
            email=email,
            user_social_provider_id=social_provider,
            **extra_fields,
        )
        user.set_unusable_password()  # type: ignore

        user.full_clean()
        user.save(using=self._db)

        user.groups.add(AuthGroup.PARTNER.value)  # type: ignore
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        이 함수는 유저 데이터를 받아 슈퍼유저를 생성합니다.

        Args:
            email (str): 이메일입니다.
            password (str): 비밀번호입니다.
            **extra_fields: 추가적인 필드입니다.

        Returns:
            User: 유저 객체입니다.
        """
        email = self.normalize_email(email)
        user = self.model(
            social_id="",
            email=email,
            is_superuser=True,
            is_admin=True,
            user_social_provider_id=UserProvider.EMAIL.value,
            **extra_fields,
        )
        user.set_password(password)  # type: ignore

        user.full_clean()
        user.save(using=self._db)

        user.groups.add(AuthGroup.SUPERUSER.value)  # type: ignore
        return user

    def create_admin(self, email: str, password: str, **extra_fields):
        """
        이 함수는 유저 데이터를 받아 관리자를 생성합니다.

        Args:
            email (str): 이메일입니다.
            password (str): 비밀번호입니다.
            **extra_fields: 추가적인 필드입니다.

        Returns:
            User: 유저 객체입니다.
        """
        email = self.normalize_email(email)
        user = self.model(
            social_id="",
            email=email,
            is_admin=True,
            user_social_provider_id=UserProvider.EMAIL.value,
            **extra_fields,
        )
        user.set_password(password)  # type: ignore

        user.full_clean()
        user.save(using=self._db)

        user.groups.add(AuthGroup.ADMIN.value)  # type: ignore
        return user
