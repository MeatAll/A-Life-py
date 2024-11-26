import random

from pygeom.geom2d import Line2D, Point2D


class TrajectoryPoint:
    """Класс - точка. Узел, соединяющий TrajectoryLine."""
    def __init__(self, point: Point2D):
        self.point = point
        self.crossroad_lines: [TrajectoryLine] = []

    def __hash__(self) -> object:
        """Получение хэш-суммы текущего экземпляра.

        :return: Хэш-сумма.
        """
        return self.point.x + self.point.y


class TrajectoryLine:
    """Класс - линия траектории, по которой перемещается отряд."""
    lines = []

    def __init__(self, start_point: TrajectoryPoint,
                 end_point: TrajectoryPoint):
        self.start_point = start_point
        self.end_point = end_point
        self.lines.append(self)
        self.line_index = len(self.lines)

    @classmethod
    def find_crossroads(cls):
        """Найти все возможные ответвления в древе
        траектории и записать их в экземпляры TrajectoryPoint."""
        for line_1 in cls.lines:
            for line_2 in cls.lines:
                if line_1.line_index != line_2.line_index:
                    result = cls.line_comparer(line_1, line_2)
                    if result == 2:
                        line_1.start_point.crossroad_lines.append(line_2)
                        line_2.end_point.crossroad_lines.append(line_1)
                    if result == 3:
                        line_1.end_point.crossroad_lines.append(line_2)
                        line_2.start_point.crossroad_lines.append(line_1)

    @classmethod
    def line_comparer(cls, a, b) -> int:
        """Компарер для линий.

        :param a: Линия 1.
        :param b: Линия 2.
        :return: 1 - если линии одинаковые.
                 2 - start_point линии 1, совпадает с end_point линии 2.
                 3 - end_point линии 1 совпадает со start_point линии 2.
                 4 - у линий нет общих точек.
                 5 - линии реверснутые друг другу."""
        if a.line_index == b.line_index:
            return 1
        a_sp: TrajectoryPoint = a.start_point
        a_ep: TrajectoryPoint = a.end_point
        b_sp: TrajectoryPoint = b.start_point
        b_ep: TrajectoryPoint = b.end_point
        if (hash(a_sp) == hash(b_sp)) and (hash(a_ep) == hash(b_ep)):
            return 1
        if (hash(a_sp) == hash(b_sp)) and (hash(a_ep) != hash(b_ep)):
            return 2
        if (hash(a_sp) != hash(b_sp)) and (hash(a_ep) == hash(b_ep)):
            return 3
        if ((hash(a_sp) != hash(b_sp)) and (hash(a_ep) != hash(b_ep)) and
                (hash(a_sp) != hash(b_ep)) and (hash(a_ep) != hash(b_sp))):
            return 4
        if (hash(a_sp) == hash(b_ep)) and (hash(a_ep) == hash(b_sp)):
            return 5


class MovingPoint:
    """Класс, обертывающий логику перемещения."""
    def __init__(self, start_point: TrajectoryPoint):
        self.trajectory_base_point: TrajectoryPoint = start_point
        self.trajectory_base_line: TrajectoryLine = self.find_current_line()
        self._moving_direction = self.get_line_direction()
        self.base_moving_step = 0.05
        self.current_moving_step = self.base_moving_step
        self.next_moving_point = None

    def find_current_line(self):
        """Найти линию траектории, к которой принадлежит текущая точка.

        :return: Экземпляр TrajectoryLine.
        """
        for line in TrajectoryLine.lines:
            line_start_point: TrajectoryPoint = line.start_point
            line_end_point: TrajectoryPoint = line.end_point
            if (hash(line_end_point) == hash(self.trajectory_base_point) or
                    hash(line_start_point) ==
                    hash(self.trajectory_base_point)):
                return line

    def get_line_direction(self):
        """Получить направление прямой, по которой двигается точка.

        :return: Вектор направления."""
        if (hash(self.trajectory_base_point) ==
                hash(self.trajectory_base_line.start_point)):
            line2d = Line2D(self.trajectory_base_line.start_point.point,
                            self.trajectory_base_line.end_point.point)
            return line2d.vec
        else:
            line2d = Line2D(self.trajectory_base_line.end_point.point,
                            self.trajectory_base_line.start_point.point)
            return line2d.vec

    def get_next_moving_cord(self):
        """Получение следующей точки,
        которая будет достигнута после окончания тика."""
        point_1 = self.trajectory_base_line.start_point
        point_2 = self.trajectory_base_line.end_point
        line_2d = Line2D(point_1.point, point_2.point)
        if line_2d.vec != self._moving_direction:
            line_2d = Line2D(point_2.point, point_1.point)
        next_point: Point2D = (
            Point2D(line_2d.ratio_point(
                self.current_moving_step).x,
                    line_2d.ratio_point(
                        self.current_moving_step).y))
        temp_line = Line2D(self.trajectory_base_point.point, next_point)
        if temp_line.length >= line_2d.length:
            next_trajectory_point: TrajectoryPoint
            if (hash(self.trajectory_base_point) ==
                    hash(self.trajectory_base_line.start_point)):
                next_trajectory_point = self.trajectory_base_line.end_point
            else:
                next_trajectory_point = self.trajectory_base_line.start_point
            crossroad_lines = next_trajectory_point.crossroad_lines
            if len(crossroad_lines) == 0:
                if (hash(self.trajectory_base_point) ==
                        hash(self.trajectory_base_line.start_point)):
                    self.trajectory_base_point = (
                        self.trajectory_base_line.end_point)
                    line_2d = (
                        Line2D(self.trajectory_base_line.end_point.point,
                               self.trajectory_base_line.start_point.point))
                    self._moving_direction = line_2d.vec
                    next_point: Point2D = (
                        Point2D(line_2d.ratio_point(
                            self.current_moving_step).x,
                                line_2d.ratio_point(
                                    self.current_moving_step).y))
                    self.next_moving_point = next_point
                else:
                    self.trajectory_base_point = (
                        self.trajectory_base_line.start_point)
                    line_2d = Line2D(
                        self.trajectory_base_line.start_point.point,
                        self.trajectory_base_line.end_point.point)
                    self._moving_direction = line_2d.vec
                    self.current_moving_step = self.base_moving_step
                    next_point: Point2D = (
                        Point2D(line_2d.
                                ratio_point(self.current_moving_step).x,
                                line_2d.
                                ratio_point(self.current_moving_step).y))
                    self.next_moving_point = next_point
            next_line_index = 0
            if len(crossroad_lines) > 1:
                next_line_index = random.randint(0, len(crossroad_lines) - 1)
            next_trajectory_line: TrajectoryLine = (
                next_trajectory_point.crossroad_lines)[next_line_index]
            self.trajectory_base_point = next_trajectory_point
            self.trajectory_base_line = next_trajectory_line
            self.current_moving_step = self.base_moving_step
            point_1 = self.trajectory_base_line.start_point
            point_2 = self.trajectory_base_line.end_point
            line_2d = Line2D(point_1.point, point_2.point)
            if line_2d.vec != self._moving_direction:
                line_2d = Line2D(point_2.point, point_1.point)
            next_point: Point2D = (
                Point2D(line_2d.ratio_point(self.current_moving_step).x,
                        line_2d.ratio_point(self.current_moving_step).y))
            self.next_moving_point = next_point
            if (hash(next_trajectory_point) ==
                    hash(next_trajectory_line.start_point)):
                self._moving_direction = (
                    Line2D(next_trajectory_point.point,
                           next_trajectory_line.end_point.point).vec)
            else:
                self._moving_direction = (
                    Line2D(next_trajectory_line.end_point.point,
                           next_trajectory_point.point).vec)
        else:
            self.current_moving_step = (
                    self.current_moving_step + self.base_moving_step)
            self.next_moving_point = next_point


if __name__ == '__main__':
    pnt = Point2D(150, 150)
    sp: TrajectoryPoint = TrajectoryPoint(pnt)

    pnt1 = Point2D(250, 250)
    en: TrajectoryPoint = TrajectoryPoint(pnt1)

    pnt2 = Point2D(400, 400)
    en2: TrajectoryPoint = TrajectoryPoint(pnt2)

    pnt3 = Point2D(600,  400)
    en3: TrajectoryPoint = TrajectoryPoint(pnt3)

    pnt4 = Point2D(400, 600)
    en4 = TrajectoryPoint(pnt4)

    tl1: TrajectoryLine = TrajectoryLine(sp, en)
    tl2: TrajectoryLine = TrajectoryLine(en, en2)
    tl3: TrajectoryLine = TrajectoryLine(en, en3)
    tl4 = TrajectoryLine(en2, en4)

    TrajectoryLine.find_crossroads()

    movingPoint = MovingPoint(sp)

    for i in range(1, 35):
        print(f"nextPoint {movingPoint.next_moving_point}")
        movingPoint.get_next_moving_cord()
