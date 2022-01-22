# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum

weekDaysMapping = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


class DateType(Enum):
    DEAD_LINE = 0
    WORK_DATE = 1
    REMINDER_DATE = 2
