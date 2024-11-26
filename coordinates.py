class Coordinates:
    """Класс - обертка координат в 2д пространстве."""
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def _set_cords(self, x: int, y: int):
        """Задание координат текущему экземпляру."""
        self._x = x
        self._y = y

    def _get_cords(self) -> object:
        """Получение координат текущего экземпляра.

        :return: Кортеж (x, y).
        """
        tpl = (self._x, self._y)
        return tpl
