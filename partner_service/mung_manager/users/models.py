from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from mung_manager.common.base.models import SimpleModel, TimeStampedModel
from mung_manager.users.managers import UserManager


class User(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    id = models.AutoField(auto_created=True, primary_key=True, db_column="user_id", serialize=False, verbose_name="유저 아이디")
    email = models.EmailField(unique=True, verbose_name="이메일")
    social_id = models.CharField(max_length=64, unique=True, blank=True, verbose_name="소셜 아이디")
    name = models.CharField(max_length=32, verbose_name="이름")
    is_active = models.BooleanField(default=True, verbose_name="활성 여부")
    is_deleted = models.BooleanField(default=False, verbose_name="삭제 여부")
    is_admin = models.BooleanField(default=False, verbose_name="관리자 여부")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="삭제 일시")
    is_agree_privacy = models.BooleanField(default=True, verbose_name="개인정보 동의 여부")
    is_agree_marketing = models.BooleanField(default=False, verbose_name="마케팅 정보 수신 동의 여부")
    gender = models.CharField(max_length=1, blank=True, verbose_name="성별")
    birth = models.DateField(blank=True, verbose_name="생년월일")
    phone_number = models.CharField(max_length=16, blank=True, verbose_name="전화번호")
    user_social_provider = models.ForeignKey(
        "UserSocialProvider",
        on_delete=models.CASCADE,
        related_name="users",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_number", "gender", "birth"]

    def __str__(self):
        return f"[{self.id}]: {self.email}"

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = "users"


class UserSocialProvider(SimpleModel):
    """
    email: 이메일 제공자
    kakao: 카카오 제공자
    """

    id = models.SmallAutoField(
        auto_created=True, primary_key=True, db_column="user_social_provider_id", serialize=False, verbose_name="유저 소셜 제공자 아이디"
    )

    def __str__(self):
        return f"[{self.id}]: {self.name}"

    class Meta:
        db_table = "T_user_social_provider"
        verbose_name = "user social provider"
        verbose_name_plural = "user social providers"
