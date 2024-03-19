import json
from typing import Any, Dict

import requests
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from mung_manager.common.exception.exceptions import AuthenticationFailedException


@define
class KakaoLoginCredentials:
    client_id: str
    client_secret: str


@define
class KakaoAccessToken:
    access_token: str


class KakaoLoginFlowService:
    """
    이 클래스는 카카오 로그인 플로우를 담당합니다.

    Attributes:
        API_URI (str): API URI입니다.
        KAKAO_AUTH_URL (str): 카카오 인증 URL입니다.
        KAKAO_ACCESS_TOKEN_OBTAIN_URL (str): 카카오 토큰 얻기 URL입니다.
        KAKAO_USER_INFO_URL (str): 카카오 유저 정보 URL입니다.
    """

    API_URI = reverse_lazy("api-auth:kakao-login-callback")

    KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_ACCESS_TOKEN_OBTAIN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    def __init__(self):
        self._credentials = kakao_login_get_credentials()

    def _get_redirect_uri(self) -> str:
        """
        이 내부 함수는 redirect_uri를 생성합니다.

        Returns:
            str: redirect_uri입니다.
        """
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def _generate_client_config(self) -> Dict[str, Any]:
        """
        이 내부 함수는 클라이언트 설정을 생성합니다.

        Returns:
            Dict[str, Any]: 클라이언트 설정입니다.
        """
        redirect_uri = self._get_redirect_uri()
        client_id = self._credentials.client_id
        return {"redirect_uri": redirect_uri, "client_id": client_id, "response_type": "code"}

    def get_authorization_url(self) -> str:
        """
        이 함수는 카카오 인증 URL을 반환합니다.

        Returns:
            str: 카카오 인증 URL입니다.
        """
        client_config = self._generate_client_config()
        response = requests.get(self.KAKAO_AUTH_URL, params=client_config)

        # 카카오 인증을 실패했을 때 예외처리
        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get authorization url from Kakao.")

        return response.url

    def get_token(self, code: str) -> KakaoAccessToken:
        """
        이 함수는 클라이언트로부터 받은 code를 이용하여 카카오 토큰 서버로부터 토큰을 얻습니다.

        Args:
            code (str): 클라이언트로부터 받은 code입니다.

        Returns:
            KakaoAccessToken: 카카오 토큰입니다.
        """
        redirect_uri = self._get_redirect_uri()
        data = {
            "grant_type": "authorization_code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "client_secret": self._credentials.client_secret,
            "code": code,
        }
        response = requests.post(self.KAKAO_ACCESS_TOKEN_OBTAIN_URL, data=data)

        # 카카오 토큰 인증을 실패했을 때 예외처리
        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get access token from Kakao.")

        kakao_token = KakaoAccessToken(access_token=response.json()["access_token"])
        return kakao_token

    def get_user_info(self, kakao_token: KakaoAccessToken) -> Dict[str, Any]:
        """
        이 함수는 카카오 토큰을 이용하요 카카오 유저 정보 서버로부터 유저 정보를 얻습니다.

        Args:
            kakao_token (KakaoAccessToken): 카카오 토큰입니다.

        Returns:
            Dict[str, Any]: 카카오 유저 정보입니다.
        """
        access_token = kakao_token.access_token
        response = requests.get(self.KAKAO_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})

        # 카카오 유저 정보를 실패했을 때 예외처리
        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get user info from Kakao.")
        return json.loads(response.text)


def kakao_login_get_credentials() -> KakaoLoginCredentials:
    """
    이 함수는 설정값으로부터 카카오 인증에 필요한 값들을 검증 후 카카오 로그인 인증 객체를 반환합니다.

    Returns:
        KakaoLoginCredentials: 카카오 로그인 인증 객체입니다.
    """
    client_id = settings.KAKAO_API_KEY
    client_secret = settings.KAKAO_SECRET_KEY

    # 카카오 인증에 필요한 값들이 없을 때 예외처리
    if not client_id:
        raise ImproperlyConfigured("KAKAO_API_KEY missing in env.")

    if not client_secret:
        raise ImproperlyConfigured("KAKAO_SECRET_KEY missing in env.")

    credentials = KakaoLoginCredentials(client_id=client_id, client_secret=client_secret)

    return credentials
