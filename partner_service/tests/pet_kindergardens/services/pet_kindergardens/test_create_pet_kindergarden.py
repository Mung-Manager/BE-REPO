from mung_manager.pet_kindergardens.services.pet_kindergardens import (
    PetKindergardenService,
)


class TestPetKindergardenService:
    """
    PetKindergardenService의 테스트 클래스

    - Test List:
        Success:
            - create_pet_kindergarden_success
    """

    def setup_method(self):
        self.pet_kindergarden_service = PetKindergardenService()

    def test_create_pet_kindergarden_success(self, active_partner_user):
        """반려동물 유치원 생성 성공 테스트

        Args:
            active_partner_user : 활성화된 파트너 유저 객체입니다.
        """
        name = "test"
        main_thumbnail_url = "http://test.com"
        profile_thumbnail_url = "http://test.com"
        phone_number = "test"
        visible_phone_number = ["test"]
        business_hours = "test"
        road_address = "test"
        abbr_address = "test"
        short_address = ["test"]
        guide_message = "test"
        latitude = 1.0
        longitude = 1.0
        reservation_available_option = "test"
        reservation_cancle_option = "test"
        daily_pet_limit = 1

        pet_kindergarden = self.pet_kindergarden_service.create_pet_kindergarden(
            user=active_partner_user,
            name=name,
            profile_thumbnail_url=profile_thumbnail_url,
            phone_number=phone_number,
            visible_phone_number=visible_phone_number,
            business_hours=business_hours,
            road_address=road_address,
            abbr_address=abbr_address,
            short_address=short_address,
            guide_message=guide_message,
            latitude=latitude,
            longitude=longitude,
            reservation_available_option=reservation_available_option,
            reservation_cancle_option=reservation_cancle_option,
            daily_pet_limit=daily_pet_limit,
            main_thumbnail_url=main_thumbnail_url,
        )

        assert pet_kindergarden.user == active_partner_user
        assert pet_kindergarden.name == name
        assert pet_kindergarden.profile_thumbnail_url == profile_thumbnail_url
        assert pet_kindergarden.phone_number == phone_number
        assert pet_kindergarden.visible_phone_number == visible_phone_number
        assert pet_kindergarden.business_hours == business_hours
        assert pet_kindergarden.road_address == road_address
        assert pet_kindergarden.abbr_address == abbr_address
        assert pet_kindergarden.short_address == short_address
        assert pet_kindergarden.guide_message == guide_message
        assert pet_kindergarden.latitude == latitude
        assert pet_kindergarden.longitude == longitude
        assert pet_kindergarden.reservation_available_option == reservation_available_option
        assert pet_kindergarden.reservation_cancle_option == reservation_cancle_option
        assert pet_kindergarden.daily_pet_limit == daily_pet_limit
        assert pet_kindergarden.main_thumbnail_url == main_thumbnail_url
