from enum import Enum
from typing import List, Tuple, Dict


# ==============================================================================
# ChoiceEnum
# ==============================================================================
class BaseChoiceEnum(Enum):
    """
    The base class for choices enumeration. This enumeration is often uses with
    Django fields.
    """

    @classmethod
    def to_tuple(cls) -> List[Tuple]:
        """
        Parse enum to tuple.
        """
        return [(data.name, data.value) for data in cls]

    @classmethod
    def to_json(cls) -> List[Dict]:
        """
        Parse enum to json.
        """
        return [{'name': data.name, 'value': data.value} for data in cls]

    @classmethod
    def values(cls) -> List[int]:
        """
        Get values of enum.
        """
        return [data.value for data in cls]

    @classmethod
    def names(cls) -> List[str]:
        """
        Get names of enum.
        """
        return [data.name for data in cls]

    @classmethod
    def get_value(cls, name: str) -> int:
        """
        Get value of enum by name.
        """
        return cls[name].value if name in cls.names() else -1

    @classmethod
    def get_name(cls, value: int) -> str:
        """
        Get name by value.
        """
        for name in cls.names():
            if cls[name].value is value:
                return name

        return ''


class CouponKindsEnum(BaseChoiceEnum):
    """
    Coupon kinds enum.
    """
    PERCENTAGE = 0
    MONEY = 1


class OrderStatusesEnum(BaseChoiceEnum):
    """
    Order statuses enum.
    """
    SHOPPING = 0
    WAITING = 1
    IN_PROGRESS = 2
    SHIPPING = 3
    PAID = 4
    CANCELED = 5


class UserRolesEnum(BaseChoiceEnum):
    """
    User roles enum.
    """
    ADMIN_ROLE = 0
    USER_ROLE = 1
    CUSTOMER_ROLE = 2


class RedeemKindsEnum(BaseChoiceEnum):
    """
    Redeem kind
    """
    NA = 0
    COUPON = 1
    POINT = 2


# This is the setting for init membership data in the database
MembershipSettings = [
    {
        'name': 'Basic',
        'require_point': 1000,
        'position': 1,
        'earning_point_rate': 0.1,
        'burning_point_rate': 1,
    },
    {
        'name': 'Silver',
        'require_point': 5000,
        'position': 2,
        'earning_point_rate': 0.1,
        'burning_point_rate': 1,
    },
    {
        'name': 'Gold',
        'require_point': 10000,
        'position': 3,
        'earning_point_rate': 0.1,
        'burning_point_rate': 1,
    },
]
