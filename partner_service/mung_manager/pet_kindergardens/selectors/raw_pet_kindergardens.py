from django.db.models.query import QuerySet
from mung_manager.pet_kindergardens.models import RawPetKindergarden
from mung_manager.pet_kindergardens.selectors.abstracts import (
    AbstractRawPetKindergardenSelector,
)


class RawPetKindergardenSelector(AbstractRawPetKindergardenSelector):
    """
    이 클래스는 로우 반려동물 유치원을 SELECT, EXISTS를 위한 클래스입니다.
    """

    def get_raw_pet_kindergarden_queryset_by_name(self, name: str) -> QuerySet[RawPetKindergarden]:
        """
        이 함수는 이름으로 로우 반려동물 유치원 쿼리셋을 조회합니다.

        Args:
            name: 반려동물 유치원 이름

        Returns:
            QuerySet[RawPetKindergarden]: 로우 반려동물 유치원 쿼리셋
        """
        return RawPetKindergarden.objects.filter(name__icontains=name)
