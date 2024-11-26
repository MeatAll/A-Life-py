import sys
from uuid import UUID

from PyQt6.QtWidgets import (QApplication, QWidget,
                             QPushButton, QLabel, QGridLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

import map_point
import squad
from map_point import MapPoint
from squad import Squad


class MainWindow(QWidget):
    """Главное окно приложения."""
    map_objects: {UUID: object} = {}

    def __init__(self):
        super().__init__()
        self.buttons: [QPushButton] = []
        self.setWindowTitle("A-Life")
        self.setFixedSize(1500, 1000)
        self.main_grid = self.create_main_grid()
        self.description_text = ''
        self.description_image = ''
        self.description_grid = (
            self.create_description_grid(self.description_image,
                                         self.description_text))
        self.main_grid.addLayout(self.description_grid, 0, 1)
        self.description_image_widget: QLabel
        self.description_text_widget: QLabel
        self.setLayout(self.main_grid)

    def create_main_grid(self) -> object:
        """Создание главной сетки разметки.

        :return: Экземпляр QGridLayout.
        """
        grid = QGridLayout(self)
        pixmap = QPixmap("garbage_map.png")
        image_label = QLabel(self)
        image_label.setPixmap(pixmap.scaled(1000, 1000))
        image_label.setScaledContents(False)
        grid.addWidget(image_label, 0, 0)
        grid.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return grid

    def create_description_grid(self, image_source: str,
                                string_source: str) -> object:
        """Создание разметки описания.

        :param image_source: Графический ресурс.
        :param string_source: Текстовый ресурс.
        :return: Экземпляр QGridLayout.
        """
        description_panel = QGridLayout(self)
        description_panel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        image_descript = QPixmap(image_source)
        descript_image_label = QLabel(self)
        descript_image_label.setPixmap(image_descript.scaled(500, 500))
        descript_image_label.setScaledContents(True)
        description_panel.addWidget(descript_image_label, 0, 0)
        self.description_image_widget = descript_image_label
        text_label = QLabel(self)
        text_label.setWordWrap(True)
        text_label.setText(string_source)
        description_panel.addWidget(text_label, 1, 0,
                                    alignment=Qt.AlignmentFlag.AlignTop)
        self.description_text_widget = text_label
        return description_panel

    def create_new_button(self, owner: object) -> object:
        """Создание новой кнопки.

        :param owner: Объект - родитель кнопки.
        :return: Экземпляр QPushButton.
        """
        x = owner._cords[0]
        y = owner._cords[1]
        var_num = len(self.buttons)
        button1 = QPushButton(f"{str(owner._uuid)}")
        button1.setFixedSize(10, 10)
        if type(owner) is MapPoint:
            button1.setStyleSheet("border-radius: 25px;")
            button1.setStyleSheet("background-color: white; "
                                  "color: yellow; font-size: 30px")
        if type(owner) is Squad:
            button1.setStyleSheet("border-radius: 15px;")
            if owner._fraction._name == "Долг":
                button1.setStyleSheet("background-color: red; "
                                      "color: black; font-size: 30px")
            if owner._fraction._name == "Свобода":
                button1.setStyleSheet("background-color: green; "
                                      "color: green; font-size: 30px")
            if owner._fraction._name == "Вольные сталкеры":
                button1.setStyleSheet("background-color: yellow; "
                                      "color: yellow; font-size: 30px")
            if owner._fraction._name == "Бандиты":
                button1.setStyleSheet("background-color: gray; "
                                      "color: gray; font-size: 30px")
        button1.clicked.connect(lambda _, x=var_num: self.button_clicked(x))
        self.main_grid.addWidget(button1, 0, 0,
                                 alignment=Qt.AlignmentFlag.AlignTop)
        self.buttons.append(button1)
        self.map_objects.update({str(owner._uuid): owner})
        self.move_button_to_start_cords(x, y, button1)
        return button1

    def move_button_to_start_cords(self, x: int, y: int, button: QPushButton):
        """Перенести кнопку в её стартовые координаты.

        :param x: Координата по Х.
        :param y: Координата по У.
        :param button: Экземпляр QPushButton.
        """
        self.main_grid.removeWidget(button)
        button.move(x, y)
        description_grid = (
            self.create_description_grid(self.description_image,
                                         self.description_text))
        self.main_grid.addLayout(description_grid, 0, 1)

    def button_clicked(self, index):
        """Событие, вызываемое при клике на кнопку.

        :param index: Внутренний индекс кнопки.
        """
        btn: QPushButton = self.buttons[index]
        if btn.text() in self.map_objects.keys():
            val = self.map_objects[btn.text()]
            if type(val) is map_point.MapPoint:
                map_pnt: map_point.MapPoint = val
                (self.description_grid.
                 removeWidget(self.description_text_widget))
                (self.description_grid.
                 removeWidget(self.description_image_widget))
                self.description_image = map_pnt._image_source
                self.description_text = map_pnt._descript
            if type(val) is squad.Squad:
                sqd: squad.Squad = val
                (self.description_grid.
                 removeWidget(self.description_text_widget))
                (self.description_grid.
                 removeWidget(self.description_image_widget))
                self.description_image = sqd._image_source
                self.description_text = sqd._descript
        description_grid = (
            self.create_description_grid(self.description_image,
                                         self.description_text))
        self.main_grid.addLayout(description_grid, 0, 1)

    def move_point(self, button: QPushButton, x, y):
        """Переместить кнопку на новые координаты.

        :param button: Экземпляр QPushButton.
        :param x: int x.
        :param y: int y.
        """
        self.main_grid.removeWidget(button)
        button.move(x, y)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
