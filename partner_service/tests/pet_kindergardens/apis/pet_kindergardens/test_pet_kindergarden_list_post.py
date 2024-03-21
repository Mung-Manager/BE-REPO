import pytest
from django.urls import reverse
from mung_manager.pet_kindergardens.enums import (
    ReservationAvailableOption,
    ReservationCancleOption,
)
from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPetKindergardenListPost(IsAuthenticateTestCase):
    """
    PetKindergardenListView의 POST 테스트 클래스

    - Test List:
        Success:
            - pet_kindergarden_list_post_success
        Fail:
            - pet_kindergarden_list_post_fail_not_authenticated
            - pet_kindergarden_list_post_fail_permission_denied
            - pet_kindergarden_list_post_fail_phone_number_validation
            - pet_kindergarden_list_post_fail_reservation_available_option_invalid_choice
            - pet_kindergarden_list_post_fail_reservation_cancle_option_invalid_choice
    """

    url = reverse("api-pet-kindergardens:pet-kindergarden-list")

    def test_pet_kindergarden_list_post_success(self, active_partner_user):
        """반려동물 유치원 리스트 POST 성공 테스트

        Args:
            active_partner_user : 활성화된 파트너 유저 객체입니다.
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        pet_kindergarden_data = {
            "name": "test",
            "main_thumbnail_url": "https://test.com",
            "profile_thumbnail_url": "https://test.com",
            "phone_number": "010-1234-5678",
            "visible_phone_number": ["010-1234-5678"],
            "business_hours": "09:00 ~ 18:00",
            "abbr_address": "서울특별시 강남구",
            "road_address": "서울특별시 강남구",
            "short_address": ["서울특별시 강남구"],
            "guide_message": "test",
            "latitude": 90,
            "longitude": 180,
            "reservation_available_option": ReservationAvailableOption.TODAY.value,
            "reservation_cancle_option": ReservationCancleOption.TODAY.value,
            "daily_pet_limit": 10,
        }

        response = self.client.post(
            self.url,
            data=pet_kindergarden_data,
            format="json",
        )

        assert response.status_code == 201
        assert response.data["data"]["name"] == pet_kindergarden_data["name"]
        assert response.data["data"]["main_thumbnail_url"] == pet_kindergarden_data["main_thumbnail_url"]
        assert response.data["data"]["profile_thumbnail_url"] == pet_kindergarden_data["profile_thumbnail_url"]
        assert response.data["data"]["phone_number"] == pet_kindergarden_data["phone_number"]
        assert response.data["data"]["visible_phone_number"] == pet_kindergarden_data["visible_phone_number"]
        assert response.data["data"]["business_hours"] == pet_kindergarden_data["business_hours"]
        assert response.data["data"]["abbr_address"] == pet_kindergarden_data["abbr_address"]
        assert response.data["data"]["road_address"] == pet_kindergarden_data["road_address"]
        assert response.data["data"]["latitude"] == pet_kindergarden_data["latitude"]
        assert response.data["data"]["longitude"] == pet_kindergarden_data["longitude"]
        assert response.data["data"]["reservation_available_option"] == pet_kindergarden_data["reservation_available_option"]
        assert response.data["data"]["reservation_cancle_option"] == pet_kindergarden_data["reservation_cancle_option"]
        assert response.data["data"]["daily_pet_limit"] == pet_kindergarden_data["daily_pet_limit"]

    def test_pet_kindergarden_list_post_fail_not_authenticated(self):
        """반려동물 유치원 리스트 POST 실패 테스트 (인증되지 않은 사용자)"""
        response = self.client.post(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_pet_kindergarden_list_post_fail_permission_denied(self, active_guest_user):
        """반려동물 유치원 리스트 POST 실패 테스트 (권한 없는 사용자)

        Args:
            active_guest_user : 활성화된 손님 유저 객체입니다.
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(self.url)

        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."

    def test_pet_kindergarden_list_post_fail_reservation_available_option_invalid_choice(self, active_partner_user):
        """반려동물 유치원 리스트 POST 실패 테스트 (예약 가능 옵션 선택지가 아닌 경우)

        Args:
            active_partner_user : 활성화된 파트너 유저 객체입니다.
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        pet_kindergarden_data = {
            "name": "test",
            "main_thumbnail_url": "https://test.com",
            "profile_thumbnail_url": "https://test.com",
            "phone_number": "010-1234-5678",
            "visible_phone_number": ["010-1234-5678"],
            "business_hours": "09:00 ~ 18:00",
            "abbr_address": "서울특별시 강남구",
            "road_address": "서울특별시 강남구",
            "short_address": ["서울특별시 강남구"],
            "guide_message": "test",
            "latitude": 90,
            "longitude": 180,
            "reservation_available_option": "test",
            "reservation_cancle_option": ReservationCancleOption.TODAY.value,
            "daily_pet_limit": 10,
        }

        response = self.client.post(
            self.url,
            data=pet_kindergarden_data,
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"reservation_available_option": ['"test" is not a valid choice.']}

    def test_pet_kindergarden_list_post_fail_reservation_cancle_option_invalid_choice(self, active_partner_user):
        """반려동물 유치원 리스트 POST 실패 테스트 (예약 취소 옵션 선택지가 아닌 경우)

        Args:
            active_partner_user : 활성화된 파트너 유저 객체입니다.
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        pet_kindergarden_data = {
            "name": "test",
            "main_thumbnail_url": "https://test.com",
            "profile_thumbnail_url": "https://test.com",
            "phone_number": "010-1234-5678",
            "visible_phone_number": ["010-1234-5678"],
            "business_hours": "09:00 ~ 18:00",
            "abbr_address": "서울특별시 강남구",
            "road_address": "서울특별시 강남구",
            "short_address": ["서울특별시 강남구"],
            "guide_message": "test",
            "latitude": 90,
            "longitude": 180,
            "reservation_available_option": ReservationAvailableOption.TODAY.value,
            "reservation_cancle_option": "test",
            "daily_pet_limit": 10,
        }

        response = self.client.post(
            self.url,
            data=pet_kindergarden_data,
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"reservation_cancle_option": ['"test" is not a valid choice.']}
