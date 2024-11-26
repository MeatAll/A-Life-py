import random
import sys
import threading
import time

from PyQt6.QtWidgets import QApplication

from pygeom.geom2d import Point2D

from fraction import Fraction
from map_point import MapPoint

from movement_trajectory import TrajectoryPoint, TrajectoryLine, MovingPoint
from squad import Squad
from view import MainWindow


class App:
    """Класс, имитирующий игровой стол."""
    wind: MainWindow
    actual_t_point: TrajectoryPoint
    t_dolg_post: TrajectoryPoint
    t_hangar: TrajectoryPoint
    t_svoboda_post: TrajectoryPoint
    t_ones_post: TrajectoryPoint
    t_agroprom_road: TrajectoryPoint
    t_baraholka: TrajectoryPoint
    t_jank_yard: TrajectoryPoint
    t_forest: TrajectoryPoint

    fraction_list = []

    @classmethod
    def create_fractions(cls):
        """Функция, создающая фракции."""
        dolg = Fraction('Долг', 100, (6, 8), (3, 4),
                        "Явно военизированная группировка, "
                        "отличающаяся строгой дисциплиной: "
                        "её члены живут фактически по уставу. "
                        "Только представители «Долга» не "
                        "торгуют уникальными порождениями Зоны с "
                        "внешним миром: по слухам, все найденные "
                        "этими людьми артефакты сдаются учёным. "
                        "Каждый долговец считает своей главной "
                        "целью защиту мира от воздействия Зоны. "
                        "Большинство операций группировки связаны с "
                        "истреблением монстров, поэтому рейды «Долга» "
                        "нередко избавляют рядовых сталкеров от многих "
                        "насущных проблем. Давно и яростно "
                        "враждует с группировкой «Свобода».",
                        "dolg/label.png")
        cls.fraction_list.append(dolg)

        svoboda = Fraction("Свобода",
                           100,
                           (7, 8),
                           (2, 3),
                           "Анархисты и сорвиголовы, объявившие "
                           "себя борцами за свободу на территории Зоны, и "
                           "поэтому постоянно конфликтующие с армейскими "
                           "подразделениями, военными сталкерами и "
                           "группировкой «Долг». Свободовцы считают, "
                           "что информацию о происходящем в Зоне нельзя "
                           "скрывать от человечества, таким образом "
                           "оспаривая монополию правительственных "
                           "организаций на владение "
                           "здешними тайнами и чудесами.",
                           "svoboda/label.png")
        cls.fraction_list.append(svoboda)

        ones = Fraction('Вольные сталкеры',
                        130,
                        (5, 9),
                        (1, 3),
                        "Сталкеры, исследующие Зону в одиночку. Таких "
                        "большинство, поскольку членство в группировке "
                        "отбирает драгоценное время, тем самым уменьшая "
                        "заработок; кроме того, некоторые просто по натуре "
                        "своей склонны к одиночеству и независимости.",
                        "ones/label.png")
        cls.fraction_list.append(ones)

        bandits = Fraction("Бандиты",
                           80,
                           (5, 7),
                           (4, 7),
                           "Представители криминального мира, "
                           "пришедшие в Зону по разным причинам: "
                           "заработать на продаже артефактов, скрыться "
                           "от закона, купить или продать оружие. В Зоне "
                           "много подобного элемента уровнем от шпаны до "
                           "серьёзных уголовников. В большинстве своём "
                           "объединены в банды. Хотя единой бандитской "
                           "организации в Зоне до сих пор нет. Сильно "
                           "докучают рядовым сталкерам.",
                           "bandits/label.png")
        cls.fraction_list.append(bandits)

    @classmethod
    def add_squad_to_fraction(cls, fraction: Fraction) -> object:
        """Добавление отряда во фракцию.

        :param fraction: Экземпляр фракции.
        :return: Экземпляр нового отряда.
        """
        squad_num = random.randint(fraction._squad_number_difference[0],
                                   fraction._squad_number_difference[1])
        squad_power = random.randint(fraction._armor_ratio_diff[0],
                                     fraction._armor_ratio_diff[1])
        init_cords = cls.t_baraholka.point
        if fraction._name == "Долг":
            init_cords = cls.t_dolg_post.point
        if fraction._name == "Свобода":
            init_cords = cls.t_svoboda_post.point
        if fraction._name == 'Вольные сталкеры':
            init_cords = cls.t_ones_post.point
        if fraction._name == "Бандиты":
            init_cords = cls.t_hangar.point
        new_squad = Squad(squad_num, squad_power, fraction._description,
                          (init_cords.x, init_cords.y),
                          fraction._image_source, fraction)
        return new_squad

    @classmethod
    def add_trajectory(cls):
        """Построение траектории перемещения."""
        dolg_post = Point2D(550, 130)
        hangar = Point2D(370, 460)
        svoboda_post = Point2D(880, 170)
        ones_post = Point2D(565, 890)
        agroprom_road = Point2D(100, 505)
        baraholka = Point2D(620, 230)
        jank_yard = Point2D(360, 790)
        forest = Point2D(810, 700)

        pnt1 = Point2D(350, 240)
        pnt2 = Point2D(480, 230)
        pnt3 = Point2D(720, 210)
        pnt4 = Point2D(250, 315)
        pnt5 = Point2D(270, 390)
        pnt6 = Point2D(380, 390)
        pnt7 = Point2D(535, 345)
        pnt8 = Point2D(615, 370)
        pnt9 = Point2D(695, 320)
        pnt10 = Point2D(770, 395)
        pnt11 = Point2D(235, 490)
        pnt12 = Point2D(490, 465)
        pnt13 = Point2D(285, 620)
        pnt14 = Point2D(395, 560)
        pnt15 = Point2D(530, 570)
        pnt16 = Point2D(730, 525)
        pnt17 = Point2D(220, 725)
        pnt18 = Point2D(580, 680)
        pnt19 = Point2D(495, 795)
        pnt20 = Point2D(640, 770)

        t_pnt1 = TrajectoryPoint(pnt1)
        t_pnt2 = TrajectoryPoint(pnt2)
        t_pnt3 = TrajectoryPoint(pnt3)
        t_pnt4 = TrajectoryPoint(pnt4)
        t_pnt5 = TrajectoryPoint(pnt5)
        t_pnt6 = TrajectoryPoint(pnt6)
        t_pnt7 = TrajectoryPoint(pnt7)
        t_pnt8 = TrajectoryPoint(pnt8)
        t_pnt9 = TrajectoryPoint(pnt9)
        t_pnt10 = TrajectoryPoint(pnt10)
        t_pnt11 = TrajectoryPoint(pnt11)
        t_pnt12 = TrajectoryPoint(pnt12)
        t_pnt13 = TrajectoryPoint(pnt13)
        t_pnt14 = TrajectoryPoint(pnt14)
        t_pnt15 = TrajectoryPoint(pnt15)
        t_pnt16 = TrajectoryPoint(pnt16)
        t_pnt17 = TrajectoryPoint(pnt17)
        t_pnt18 = TrajectoryPoint(pnt18)
        t_pnt19 = TrajectoryPoint(pnt19)
        t_pnt20 = TrajectoryPoint(pnt20)

        cls.t_dolg_post = TrajectoryPoint(dolg_post)
        cls.t_hangar = TrajectoryPoint(hangar)
        cls.t_svoboda_post = TrajectoryPoint(svoboda_post)
        cls.t_ones_post = TrajectoryPoint(ones_post)
        cls.t_agroprom_road = TrajectoryPoint(agroprom_road)
        cls.t_baraholka = TrajectoryPoint(baraholka)
        cls.t_jank_yard = TrajectoryPoint(jank_yard)
        cls.t_forest = TrajectoryPoint(forest)

        TrajectoryLine(cls.t_dolg_post, t_pnt2)
        TrajectoryLine(cls.t_dolg_post, t_pnt3)
        TrajectoryLine(t_pnt1, t_pnt2)
        TrajectoryLine(t_pnt1, t_pnt4)
        TrajectoryLine(t_pnt2, cls.t_baraholka)
        TrajectoryLine(t_pnt3, cls.t_baraholka)
        TrajectoryLine(cls.t_svoboda_post, t_pnt3)
        TrajectoryLine(t_pnt4, t_pnt5)
        TrajectoryLine(t_pnt5, t_pnt6)
        TrajectoryLine(t_pnt6, t_pnt7)
        TrajectoryLine(t_pnt2, t_pnt7)
        TrajectoryLine(t_pnt7, t_pnt8)
        TrajectoryLine(t_pnt8, t_pnt9)
        TrajectoryLine(t_pnt3, t_pnt9)
        TrajectoryLine(t_pnt5, t_pnt11)
        TrajectoryLine(cls.t_agroprom_road, t_pnt11)
        TrajectoryLine(t_pnt11, cls.t_hangar)
        TrajectoryLine(cls.t_hangar, t_pnt12)
        TrajectoryLine(t_pnt12, t_pnt7)
        TrajectoryLine(t_pnt12, t_pnt15)
        TrajectoryLine(t_pnt9, t_pnt10)
        TrajectoryLine(t_pnt10, t_pnt16)
        TrajectoryLine(t_pnt11, t_pnt13)
        TrajectoryLine(t_pnt13, t_pnt14)
        TrajectoryLine(t_pnt14, t_pnt15)
        TrajectoryLine(t_pnt13, t_pnt17)
        TrajectoryLine(t_pnt13, cls.t_jank_yard)
        TrajectoryLine(cls.t_jank_yard, t_pnt19)
        TrajectoryLine(t_pnt19, t_pnt18)
        TrajectoryLine(t_pnt18, t_pnt15)
        TrajectoryLine(t_pnt19, t_pnt20)
        TrajectoryLine(t_pnt20, cls.t_forest)
        TrajectoryLine(cls.t_forest, t_pnt16)
        TrajectoryLine(t_pnt19, cls.t_ones_post)

        TrajectoryLine.find_crossroads()

    @staticmethod
    def convert_tr_point_to_map_point(tr_point: TrajectoryPoint,
                                      descript: str, image: str) -> object:
        """Конвертировать экземпляр TrajectoryPoint в MapPoint.

        :param tr_point: Экземпляр TrajectoryPoint.
        :param descript: Описание точки.
        :param image: Изображение точки.
        :return: Экземпляр MapPoint.
        """
        mp_point = MapPoint(descript,
                            (tr_point.point.x, tr_point.point.y), image)
        return mp_point

    @classmethod
    def create_threat(cls, squad_button: object):
        """Метод, используемый при создании потоков.

        :param squad_button: Экземпляр QPushButton.
        """
        movingPoint = MovingPoint(cls.actual_t_point)
        while True:
            movingPoint.get_next_moving_cord()
            cords: Point2D = movingPoint.next_moving_point
            if cords is not None:
                time.sleep(1.5)
                cls.wind.move_point(squad_button, int(cords.x), int(cords.y))


if __name__ == '__main__':
    App.create_fractions()
    App.add_trajectory()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    mp_dolg_post = (
        App.convert_tr_point_to_map_point(
            App.t_dolg_post,
            'На этом месте стоит блокпост, '
            'принадлежащий группировке Долг. '
            'На этом блокпосте, называемом '
            '«Заставой», бойцы Долга проводят '
            'первичный «фейсконтроль» '
            'посетителей их территории. '
            'В блокпосте стоят два вагона '
            'и сдвижные ворота.',
            "dolg_post.png"))

    window.create_new_button(mp_dolg_post)

    mp_svoboda_post = (
        App.convert_tr_point_to_map_point(
            App.t_svoboda_post,
            'Блокпост на северо-востоке Свалки. '
            'Является переходом в Тёмную долину. '
            'В 2012 году блокпост был полностью '
            'опустошён, и это место стало '
            'непригодным для лагеря. '
            'Появился повышенный радиационный фон, '
            'а чуть южнее часто бродят голодные собаки. '
            'Чаще всего здесь будут встречаться бандиты, '
            'следующие на Свалку.',
            "svoboda_post.png"))
    window.create_new_button(mp_svoboda_post)

    mp_hangar = (
        App.convert_tr_point_to_map_point(
            App.t_hangar,
            "Представляет собой сооружение "
            "из сборного железобетона, "
            "с просторным двором, "
            "обнесенный кирпичной стеной. "
            "Крыша здания была частично "
            "обрушена в результате падения "
            "рядом стоящего во дворе ангара "
            "крана БК-100. Внутри двора есть "
            "разгрузочная площадка для автомобилей. "
            "Ангар является частью железнодорожной "
            "инфраструктуры — внутри есть два "
            "тупиковых пути, на которых хаотично "
            "стоят товарные вагоны, а часть пола "
            "справа и слева от путей стала "
            "автомобильным проездом, видимо, "
            "служившим для перегрузки грузов "
            "в вагоны. Чтобы как-то оправдать "
            "назначение этого здания, ворота "
            "на восточном входе получили "
            "символику железнодорожного транспорта "
            "(молоток, скрещенный с разводным ключом). "
            "Через дорогу напротив ворот стоит "
            "автобусная остановка, в которой "
            "отдыхают сталкеры.",
            "hangar"))
    window.create_new_button(mp_hangar)

    mp_forest = (
        App.convert_tr_point_to_map_point(
            App.t_forest,
            'Локация имеет желтые оттенки лесостепи, '
            'практически кроме тополей на локации деревьев нет. '
            'Некоторое подобие растительности есть на '
            'юго-востоке локации и на юго-западе; '
            'в самом дальнем конце леса на '
            'юго-востоке на ветках и на земле '
            'были разбросаны трупы сталкеров.',
            'forest.png'))
    window.create_new_button(mp_forest)

    mp_ones_post = (
        App.convert_tr_point_to_map_point(
            App.t_ones_post,
            'Блокпост-приемник — блокпост, '
            'встречающийся при переходе с Кордона на Свалку.',
            'ones_post.png'))
    window.create_new_button(mp_ones_post)

    mp_baraholka = (
        App.convert_tr_point_to_map_point(
            App.t_baraholka,
            "Барахолка — полуразрушенное "
            "здание на севере Свалки. В 2011 "
            "году это действительно была Барахолка, "
            "но в 2012 после второго Большого выброса "
            "основа здания окончательно обрушилась и "
            "усыпана аномалиями.",
            "baraholka.png"))
    window.create_new_button(mp_baraholka)

    mp_agroprom_road = (
        App.convert_tr_point_to_map_point(
            App.t_agroprom_road,
            "Тропинка, некогда безопасная, "
            "ведущая со свалки брошенной техники "
            "а локацию НИИ «Агропром». Рядом с "
            "тропинкой расположен опорный пункт "
            "бандитов на Свалке.",
            'agroprom_road'))
    window.create_new_button(mp_agroprom_road)

    mp_jank_yard = (
        App.convert_tr_point_to_map_point(
            App.t_jank_yard,
            'Небольшая территория, '
            'огражденная забором с колючей проволокой. '
            'У входа стоит будочка, горит костер. '
            'Со всех сторон место ограждено '
            'колючей проволокой, '
            'в нескольких местах есть выходы. '
            'Много брошенной техники, '
            'откуда и название.',
            'junk_yard.png'))
    window.create_new_button(mp_jank_yard)

    App.wind = window

    threats = []

    for fr in App.fraction_list:
        if fr._mans_in_squad < (fr._number / 3):
            if fr._name == 'Долг':
                new_squad1 = App.add_squad_to_fraction(fr)
                squad_button1 = window.create_new_button(new_squad1)
                App.actual_t_point = App.t_dolg_post
                my_thread1 = threading.Thread(target=App.create_threat,
                                              args=(squad_button1, ))
                my_thread1.start()
                threats.append(my_thread1)
            if fr._name == "Свобода":
                new_squad2 = App.add_squad_to_fraction(fr)
                squad_button2 = window.create_new_button(new_squad2)
                App.actual_t_point = App.t_svoboda_post
                my_thread2 = threading.Thread(target=App.create_threat,
                                              args=(squad_button2, ))
                my_thread2.start()
                threats.append(my_thread2)
            if fr._name == 'Вольные сталкеры':
                new_squad3 = App.add_squad_to_fraction(fr)
                squad_button3 = window.create_new_button(new_squad3)
                App.actual_t_point = App.t_ones_post
                my_thread3 = threading.Thread(target=App.create_threat,
                                              args=(squad_button3, ))
                my_thread3.start()
                threats.append(my_thread3)
            if fr._name == 'Бандиты':
                new_squad4 = App.add_squad_to_fraction(fr)
                squad_button4 = window.create_new_button(new_squad4)
                App.actual_t_point = App.t_hangar
                my_thread4 = threading.Thread(target=App.create_threat,
                                              args=(squad_button4, ))
                my_thread4.start()
                threats.append(my_thread4)

    sys.exit(app.exec())
