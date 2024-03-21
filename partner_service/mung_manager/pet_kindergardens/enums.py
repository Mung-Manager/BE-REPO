from enum import Enum


class ReservationAvailableOption(Enum):
    """
    예약 가능 옵션
    """

    TODAY = "당일 예약 가능"
    BEFORE_ONE_DAY = "1일 전 예약 가능"
    BEFORE_TWO_DAY = "2일 전 예약 가능"
    BEFORE_THREE_DAY = "3일 전 예약 가능"
    BEFORE_FOUR_DAY = "4일 전 예약 가능"
    BEFORE_FIVE_DAY = "5일 전 예약 가능"


class ReservationCancleOption(Enum):
    """
    예약 취소 옵션
    """

    TODAY = "당일 취소 가능"
    BEFORE_TWELVE_HOUR = "12시간 전 취소 가능"
    BEFORE_ONE_DAY = "1일 전 취소 가능"
    BEFORE_TWO_DAY = "2일 전 취소 가능"
    BEFORE_THREE_DAY = "3일 전 취소 가능"
    BEFORE_FOUR_DAY = "4일 전 취소 가능"
    BEFORE_FIVE_DAY = "5일 전 취소 가능"


class TicketType(Enum):
    """
    티켓 타입
    """

    TIME = "시간"
    ALL_DAY = "종일"
    HOTEL = "호텔"
