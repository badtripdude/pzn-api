from enum import Enum


class Gender(Enum):
    SENIOR_CHILD = 7  # Старший ребенок
    MIDDLE_CHILD = 6  # Средний ребенок
    BABY = 5  # Малыш
    CHILD = 4  # Ребенок
    FEMALE = 3  # Женский
    MALE = 2  # Мужской
    UNISEX = 1  # Унисекс


class SortDirection(Enum):
    DESCENDING = 1  # Убывание
    ASCENDING = 0  # Возрастание


class SalesData(Enum):
    SALES_LAST_7_DAYS = 101
    RELEASE_DATE = 3
    PRICE = 2
    SALES = 1
    RECOMMENDED = 0
