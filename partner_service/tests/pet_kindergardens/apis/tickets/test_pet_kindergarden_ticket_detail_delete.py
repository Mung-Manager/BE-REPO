import pytest
from django.urls import reverse
from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPetKindergardenTicketDetailDelete(IsAuthenticateTestCase):
    """
    PetKindergardenTicketDetailView의 DELETE 테스트 클래스

    - Test List:
        Success:
            - pet_kindergarden_ticket_detail_delete_success
        Fail:
            - pet_kindergarden_ticket_detail_delete_fail_not_authenticated
            - pet_kindergarden_ticket_detail_delete_fail_permission_denied
    """

    def test_pet_kindergarden_ticket_detail_delete_success(self, ticket):
        """반려동물 유치원 티켓 디테일 DELETE 성공 테스트

        Args:
            ticket : 티켓입니다.
        """
        access_token = self.obtain_token(ticket.pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        response = self.client.delete(
            reverse(
                "api-pet-kindergardens:pet-kindergarden-tickets-detail",
                kwargs={"pet_kindergarden_id": ticket.pet_kindergarden.id, "ticket_id": ticket.id},
            ),
        )
        assert response.status_code == 204

    def test_pet_kindergarden_ticket_detail_delete_fail_not_authenticated(self, ticket):
        """반려동물 유치원 티켓 디테일 DELETE 실패 테스트 (인증되지 않은 경우)

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
        """
        response = self.client.delete(
            reverse(
                "api-pet-kindergardens:pet-kindergarden-tickets-detail",
                kwargs={"pet_kindergarden_id": ticket.pet_kindergarden.id, "ticket_id": ticket.id},
            ),
        )
        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_pet_kindergarden_ticket_detail_delete_fail_permission_denied(self, ticket, active_guest_user):
        """반려동물 유치원 티켓 디테일 DELETE 실패 테스트 (권한이 없는 경우)

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
            active_user : 활성화된 유저 객체입니다.
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)

        response = self.client.delete(
            reverse(
                "api-pet-kindergardens:pet-kindergarden-tickets-detail",
                kwargs={"pet_kindergarden_id": ticket.pet_kindergarden.id, "ticket_id": ticket.id},
            ),
        )
        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."
