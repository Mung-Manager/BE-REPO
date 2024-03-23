from django.contrib.gis.geos import Point
from django.db import transaction
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

    @transaction.atomic
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
        detail_address: str,
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
            name (str): 반려동물 유치원 이름입니다.
            profile_thumbnail_url (str): 프로필 썸네일 URL입니다.
            phone_number (str): 전화번호입니다.
            visible_phone_number (list[str]): 보이는 전화번호입니다.
            business_hours (str): 영업시간입니다.
            road_address (str): 도로명 주소입니다.
            abbr_address (str): 간략 주소입니다.
            detail_address (str): 상세 주소입니다.
            short_address (list[str]): 짧은 주소입니다.
            guide_message (str): 가이드 메시지입니다.
            latitude (float): 위도입니다.
            longitude (float): 경도입니다.
            reservation_available_option (str): 예약 가능 옵션입니다.
            reservation_cancle_option (str): 예약 취소 옵션입니다.
            daily_pet_limit (int): 일일 반려동물 제한입니다.
            main_thumbnail_url (str): 메인 썸네일 URL입니다.

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
            detail_address=detail_address,
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
