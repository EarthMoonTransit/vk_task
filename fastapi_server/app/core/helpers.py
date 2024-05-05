from enum import Enum


class Env(Enum):
    """Название окружения"""

    prod = "prod"
    preprod = "preprod"
    stage = "stage"


class Domain(Enum):
    """Тип пользователя"""

    master = "master"
    slave = "slave"
