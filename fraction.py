class Fraction:
    """Класс - объект, представляющий фракцию."""
    def __init__(self, name: str,
                 number: int,
                 armor_ratio_difference: tuple[int],
                 squad_number_difference: tuple[int],
                 description: str,
                 image: str):
        """Инициализация нового экземпляра Fraction.

        :param name: Название фракции.
        :param number: Количество человек.
        :param armor_ratio_difference: Разброс по оружию.
        :param squad_number_difference: Разбор по численности отряда.
        :param description:Текстовое описание.
        :param image: Графическое изображение.
        """
        self._description = description
        self._image_source = image
        self._name = name
        self._number = number
        self._armor_ratio_diff = armor_ratio_difference
        self._squad_number_difference = squad_number_difference
        self._mans_in_squad = 0

    def _squad_die(self, man_in_squad: int) -> object:
        """Метод - убийство отряда.

        :param man_in_squad: Сколько человек было в отряде.
        :return: Сколько человек осталось во фракции.
        """
        self._number = self._number - man_in_squad
        return self._number

    def _add_mans(self, new_mans_num: int) -> object:
        """Добавить людей в группировку.

        :param new_mans_num: Сколько человек добавить.
        :return: Новое количество людей во фракции.
        """
        self._number = self._number + new_mans_num
        return self._number

    def _can_add_squad(self, number: int) -> object:
        """Проверка на возможность добавления нового отряда.

        :param number: Из скольки человек состоит новый отряд.
        :return: true/false.
        """
        if (self._number - self._mans_in_squad) >= number:
            return True
        else:
            return False
