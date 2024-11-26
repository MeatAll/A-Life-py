from coordinates import Coordinates
from fraction import Fraction
from map_point import MapPoint


class Squad(MapPoint):
    """Класс - обертка отряда."""
    def __init__(self, number: int, power: int, descript: str,
                 init_cords: Coordinates, image: str,
                 parent_fraction: Fraction):
        """Инициализация нового экземпляра отряда.

        :param number: Количество человек в отряде.
        :param power: Коэффициент силы оружия.
        :param descript: Текстовое описание отряда.
        :param init_cords: Начальные координаты.
        :param image: Картинка отряда.
        :param parent_fraction: Экземпляр группировки,
                          к которой принадлежит отряд.
        """
        self._number = number
        self._power = power
        self._fraction = parent_fraction
        super().__init__(descript, init_cords, image)
