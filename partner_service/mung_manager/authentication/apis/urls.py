from django.urls import path
from mung_manager.authentication.apis.views import (
    KakaoLoginRedirectView,
    KakaoLoginView,
    UserJWTRefreshView,
)

urlpatterns = [
    # auth
    path("/jwt/refresh", UserJWTRefreshView.as_view(), name="jwt-refresh"),
    # oauth
    path("/kakao/callback", KakaoLoginView.as_view(), name="kakao-login-callback"),
    path("/kakao/redirect", KakaoLoginRedirectView.as_view(), name="kakao-login-redirect"),
]
