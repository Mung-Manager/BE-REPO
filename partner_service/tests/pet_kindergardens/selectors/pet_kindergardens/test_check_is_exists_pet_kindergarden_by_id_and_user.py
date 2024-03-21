import pytest
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)

pytestmark = pytest.mark.django_db


class TestCheckIsExistsPetKindergardenByIdAndUser:
    """
    PetKindergardenSelector의 check_is_exists_pet_kindergarden_by_id_and_user 테스트 클래스

    - Test List:
        Success:
            - check_is_exists_pet_kindergarden_by_id_and_user_success
        Fail:
            - check_is_exists_pet_kindergarden_by_id_and_user_fail_does_not_exist
    """

    def setup_method(self):
        self.pet_kindergarden_selector = PetKindergardenSelector()

    def test_check_is_exists_pet_kindergarden_by_id_and_user_success(self, pet_kindergarden):
        """아이디와 유저로 반려동물 유치원 존재 확인 성공 테스트

        Args:
            pet_kindergarden : 반려동물 유치원입니다.
        """
        is_exists = self.pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
            pet_kindergarden.id, pet_kindergarden.user
        )
        assert is_exists is True

    def test_check_is_exists_pet_kindergarden_by_id_and_user_fail_does_not_exist(self):
        """아이디와 유저로 반려동물 유치원 존재 확인 실패 테스트 (존재하지 않는 반려동물 유치원)"""
        is_exists = self.pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(999, None)
        assert is_exists is False
