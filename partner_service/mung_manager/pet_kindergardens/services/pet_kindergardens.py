from django.contrib.gis.geos import Point
from mung_manager.pet_kindergardens.models import PetKindergarden
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)


class PetKindergardenService:
    """
    이 클래스는 반려동물 유치원과 관련된 비즈니스 로직을 담당합니다.
    """

    def __init__(self):
        self.pet_kindergarden_selector = PetKindergardenSelector()

    def create_pet_kindergarden(
        self,
        user,
        name: str,
        profile_thumbnail_url: str,
        phone_number: str,
        visible_phone_number: list[str],
        business_hours: str,
        road_address: str,
        abbr_address: str,
        short_address: list[str],
        guide_message: str,
        latitude: float,
        longitude: float,
        reservation_available_option: str,
        reservation_cancle_option: str,
        daily_pet_limit: int,
        main_thumbnail_url: str,
    ) -> PetKindergarden:
        """
        이 함수는 반려동물 유치원 데이터를 받아 반려동물 유치원을 생성합니다.

        Args:
            user (User): 유저 객체입니다.
            data (OrderedDict): 반려동물 유치원 생성 데이터입니다.

        Returns:
            PetKindergarden: 반려동물 유치원 객체입니다.
        """
        pet_kindergarden = PetKindergarden(
            name=name,
            profile_thumbnail_url=profile_thumbnail_url,
            main_thumbnail_url=main_thumbnail_url,
            phone_number=phone_number,
            visible_phone_number=visible_phone_number,
            business_hours=business_hours,
            road_address=road_address,
            abbr_address=abbr_address,
            short_address=short_address,
            guide_message=guide_message,
            latitude=latitude,
            longitude=longitude,
            point=Point(longitude, latitude),
            reservation_available_option=reservation_available_option,
            reservation_cancle_option=reservation_cancle_option,
            daily_pet_limit=daily_pet_limit,
            user=user,
        )

        # 반려동물 유치원 데이터를 검증 후 저장
        pet_kindergarden.full_clean()
        pet_kindergarden.save()

        return pet_kindergarden
