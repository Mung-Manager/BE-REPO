from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from mung_manager.common.base.models import TimeStampedModel
from mung_manager.pet_kindergardens.enums import (
    ReservationAvailableOption,
    ReservationCancleOption,
    TicketType,
)
from mung_manager.users.models import User


class PetKindergarden(TimeStampedModel):
    id = models.AutoField(auto_created=True, primary_key=True, db_column="pet_kindergarden_id", serialize=False, verbose_name="펫 유치원 아이디")
    name = models.CharField(max_length=64, verbose_name="유치원 이름")
    main_thumbnail_url = models.URLField(verbose_name="메인 썸네일")
    profile_thumbnail_url = models.URLField(verbose_name="프로필 썸네일 이미지")
    phone_number = models.CharField(max_length=16, verbose_name="전화번호", blank=True)
    visible_phone_number = ArrayField(models.CharField(max_length=16), verbose_name="노출 전화번호", size=2)
    business_hours = models.CharField(max_length=64, verbose_name="영업 시간")
    road_address = models.CharField(max_length=128, verbose_name="도로명 주소")
    abbr_address = models.CharField(max_length=128, verbose_name="지번 주소")
    detail_address = models.CharField(max_length=128, verbose_name="상세 주소", blank=True)
    short_address = ArrayField(models.CharField(max_length=128), verbose_name="간단 주소", size=10)
    guide_message = models.TextField(verbose_name="안내 메시지", blank=True)
    latitude = models.DecimalField(max_digits=13, decimal_places=10, verbose_name="위도")
    longitude = models.DecimalField(max_digits=13, decimal_places=10, verbose_name="경도")
    point = PointField(verbose_name="위치 좌표")
    reservation_available_option = models.CharField(
        max_length=64, verbose_name="예약 가능 옵션", choices=[(o.value, o.name) for o in ReservationAvailableOption]
    )
    reservation_cancle_option = models.CharField(
        max_length=64, verbose_name="예약 취소 옵션", choices=[(o.value, o.name) for o in ReservationCancleOption]
    )
    daily_pet_limit = models.SmallIntegerField(verbose_name="일일 펫 제한")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pet_kindergardens",
    )

    def __str__(self):
        return f"[{self.id}]: {self.name}"

    class Meta:
        db_table = "pet_kindergarden"
        verbose_name = "pet kindergarden"
        verbose_name_plural = "pet kindergarden"


class RawPetKindergarden(models.Model):
    """
    반려동물 유치원 raw 데이터 (네이버 지도 데이터)
    """

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    thum_url = models.URLField(db_column="thumUrl")
    tel = models.CharField(max_length=16, db_column="tel")
    virtual_tel = models.CharField(max_length=16, blank=True, db_column="virtualTel")
    name = models.CharField(max_length=64, db_column="name")
    x = models.DecimalField(max_digits=13, decimal_places=10, db_column="x")
    y = models.DecimalField(max_digits=13, decimal_places=10, db_column="y")
    business_hours = models.CharField(max_length=64, db_column="businessHours")
    address = models.CharField(max_length=128, db_column="address")
    road_address = models.CharField(max_length=128, db_column="roadAddress")
    abbr_address = models.CharField(max_length=128, db_column="abbrAddress")
    short_address = ArrayField(models.CharField(max_length=128), size=10, db_column="shortAddress")

    def __str__(self):
        return f"[{self.id}]: {self.name}"

    class Meta:
        db_table = "raw_pet_kindergarden"
        verbose_name = "raw pet kindergarden"
        verbose_name_plural = "raw pet kindergarden"


class Ticket(TimeStampedModel):
    id = models.AutoField(auto_created=True, primary_key=True, db_column="ticket_id", serialize=False, verbose_name="티켓 아이디")
    usage_time = models.IntegerField(verbose_name="사용 시간")
    usage_count = models.IntegerField(verbose_name="사용 횟수")
    usage_period_in_days = models.IntegerField(verbose_name="사용 기간(일)")
    price = models.IntegerField(verbose_name="금액")
    ticket_type = models.CharField(max_length=32, verbose_name="티켓 타입", choices=[(t.value, t.name) for t in TicketType])
    deleted_at = models.DateTimeField(verbose_name="삭제 일시", blank=True, null=True)
    is_deleted = models.BooleanField(verbose_name="삭제 여부", default=False)
    pet_kindergarden = models.ForeignKey(
        PetKindergarden,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    def __str__(self):
        return f"[{self.id}]: {self.pet_kindergarden.name} - {self.ticket_type}"

    class Meta:
        db_table = "ticket"
        verbose_name = "ticket"
        verbose_name_plural = "tickets"
