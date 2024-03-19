from typing import TYPE_CHECKING, Sequence, Type

from mung_manager.common.authentication import CustomJWTAuthentication
from mung_manager.common.permissions import IsPartnerPermission
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission

if TYPE_CHECKING:
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class APIAuthMixin:
    """
    이 클래스는 API의 인가 및 인증을 처리하는 Mixin입니다.
    """

    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        CustomJWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsPartnerPermission,)
