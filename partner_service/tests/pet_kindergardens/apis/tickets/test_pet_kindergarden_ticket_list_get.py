import pytest
from django.urls import reverse
from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPetKindergardenTicketListGet(IsAuthenticateTestCase):
    """
    PetKindergardenTicketListView의 GET 테스트 클래스

    - Test List:
        Success:
            - pet_kindergarden_ticket_list_get_success
        Fail:
            - pet_kindergarden_ticket_list_get_fail_not_authenticated
            - pet_kindergarden_ticket_list_get_fail_permission_denied
    """

    def test_pet_kindergarden_ticket_list_get_success(self, ticket):
        """반려동물 유치원 티켓 리스트 GET 성공 테스트

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
        """
        access_token = self.obtain_token(ticket.pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        response = self.client.get(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": ticket.pet_kindergarden.id}),
        )
        assert response.status_code == 200
        assert response.data["data"][0]["id"] == ticket.id
        assert response.data["data"][0]["ticket_type"] == ticket.ticket_type
        assert response.data["data"][0]["usage_time"] == ticket.usage_time
        assert response.data["data"][0]["usage_count"] == ticket.usage_count
        assert response.data["data"][0]["usage_period_in_days"] == ticket.usage_period_in_days
        assert response.data["data"][0]["price"] == ticket.price
        assert response.data["data"][0]["is_deleted"] == ticket.is_deleted

    def test_pet_kindergarden_ticket_list_get_fail_not_authenticated(self, pet_kindergarden):
        """반려동물 유치원 티켓 리스트 GET 실패 테스트 (인증되지 않은 경우)

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
        """
        response = self.client.get(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": pet_kindergarden.id}),
        )
        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_pet_kindergarden_ticket_list_get_fail_permission_denied(self, pet_kindergarden, active_guest_user):
        """반려동물 유치원 티켓 리스트 GET 실패 테스트 (권한이 없는 경우)

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

    def test_pet_kindergarden_ticket_list_get_fail_does_not_exist(self, pet_kindergarden):
        """반려동물 유치원 티켓 리스트 GET 실패 테스트 (존재하지 않는 유치원인 경우)

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
        """
        access_token = self.obtain_token(pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        response = self.client.get(
            reverse("api-pet-kindergardens:pet-kindergarden-tickets-list", kwargs={"pet_kindergarden_id": 999}),
        )
        assert response.status_code == 404
        assert response.data["code"] == "not_found_pet_kindergarden"
        assert response.data["message"] == "PetKindergarden does not exist."
