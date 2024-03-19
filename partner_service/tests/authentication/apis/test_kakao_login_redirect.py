import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestKakaoLoginRedirectAPI:
    """
    KakaoLoginRedirect의 GET 테스트 클래스

    - Test List:
        Success:
            - kakao_login_redirect_api_success

    """

    url = reverse("api-auth:kakao-login-redirect")

    def test_kakao_login_redirect_api_success(self, api_client, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.url = "https://kauth.kakao.com/oauth/authorize"

        mocker.patch("mung_manager.authentication.services.kakao_oauth.requests.get", return_value=mock_response)

        response = api_client.get(path=self.url)

        assert response.status_code == 302
        assert response.url == "https://kauth.kakao.com/oauth/authorize"
