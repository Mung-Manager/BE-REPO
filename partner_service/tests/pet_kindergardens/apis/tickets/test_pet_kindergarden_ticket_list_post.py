import pytest
from django.urls import reverse
from mung_manager.pet_kindergardens.enums import TicketType
from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPetKindergardenTicketListPost(IsAuthenticateTestCase):
    """
    PetKindergardenTicketListView의 POST 테스트 클래스

    - Test List:
        Success:
            - pet_kindergarden_ticket_list_post_success
        Fail:
            - pet_kindergarden_ticket_list_post_fail_not_authenticated
            - pet_kindergarden_ticket_list_post_fail_permission_denied
            - pet_kindergarden_ticket_list_post_fail_pet_kindergarden_does_not_exist
            - pet_kindergarden_ticket_list_post_fail_ticket_type_invalid_choice
    """

    def test_pet_kindergarden_ticket_list_post_success(self, pet_kindergarden):
        """반려동물 유치원 티켓 리스트 POST 성공 테스트

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
        """
        access_token = self.obtain_token(pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        pet_kindergarden_ticket_data = {
            "ticket_type": TicketType.TIME.value,
            "usage_time": 10,
            "usage_count": 10,
            "usage_period_in_days": 10,
            "price": 10000,
        }

        response = self.client.post(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
            data=pet_kindergarden_ticket_data,
            format="json",
        )
        assert response.status_code == 201
        assert response.data["data"]["ticket_type"] == TicketType.TIME.value
        assert response.data["data"]["usage_time"] == 10
        assert response.data["data"]["usage_count"] == 10
        assert response.data["data"]["usage_period_in_days"] == 10
        assert response.data["data"]["price"] == 10000
        assert not response.data["data"]["is_deleted"]

    def test_pet_kindergarden_ticket_list_post_fail_not_authenticated(self, pet_kindergarden):
        """반려동물 유치원 티켓 리스트 POST 실패 테스트 (인증되지 않은 경우)

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
        """
        response = self.client.post(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
            data={},
            format="json",
        )
        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_pet_kindergarden_ticket_list_post_fail_permission_denied(self, pet_kindergarden, active_guest_user):
        """반려동물 유치원 티켓 리스트 POST 실패 테스트 (권한이 없는 경우)

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
            active_user : 활성화된 유저 객체입니다.
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)

        response = self.client.get(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
        )
        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."

    def test_pet_kindergarden_ticket_list_post_fail_pet_kindergarden_does_not_exist(self, active_partner_user):
        """반려동물 유치원 티켓 리스트 POST 실패 테스트 (존재하지 않는 유치원)

        Args:
            active_partner_user : 활성화된 파트너 유저 객체입니다.
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        pet_kindergarden_ticket_data = {
            "ticket_type": TicketType.TIME.value,
            "usage_time": 10,
            "usage_count": 10,
            "usage_period_in_days": 10,
            "price": 10000,
        }

        response = self.client.post(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": 1}),
            data=pet_kindergarden_ticket_data,
            format="json",
        )
        assert response.status_code == 404
        assert response.data["code"] == "not_found_pet_kindergarden"
        assert response.data["message"] == "PetKindergarden does not exist."

    def test_pet_kindergarden_ticket_list_post_fail_ticket_type_invalid_choice(self, pet_kindergarden):
        """반려동물 유치원 티켓 리스트 POST 실패 테스트 (티켓 타입이 선택지가 아닌 경우)

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
        """
        access_token = self.obtain_token(pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        pet_kindergarden_ticket_data = {
            "ticket_type": "invalid_choice",
            "usage_time": 10,
            "usage_count": 10,
            "usage_period_in_days": 10,
            "price": 10000,
        }

        response = self.client.post(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
            data=pet_kindergarden_ticket_data,
            format="json",
        )
        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"ticket_type": ['"invalid_choice" is not a valid choice.']}
