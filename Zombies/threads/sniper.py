from PyQt4 import QtCore, QtGui
from math import atan2, degrees, sqrt
from itertools import cycle
from threads.balas import Bala


class Sniper:

    def __init__(self, main, label):
        self.label = label
        self.main = main
        self.size = self.main.pics["p1"].size()
        self.cambiar_imagen(self.main.pics["p3"])

        self.vector_mouse = (1, 0)
        self.x_mouse = 565
        self.y_mouse = 285
        self.theta = 0

        self._pics = cycle([self.main.pics["p" + str(i)] for i in range(1, 5)])
        self.current_pic = self.main.pics["p3"]
        self.balas = []

    def mover(self, direccion):
        x = self.label.x()
        y = self.label.y()
        _x = self.vector_mouse[0] * 3
        _y = self.vector_mouse[1] * 3
        __x = - _y
        __y = _x
        if direccion == "U":
            dif_x, dif_y = (x + _x, y - _y)
        elif direccion == "D":
            dif_x, dif_y = (x - _x, y + _y)
        elif direccion == "R":
            dif_x, dif_y = (x - __x, y + __y)
        elif direccion == "L":
            dif_x, dif_y = (x + __x, y - __y)

        if dif_x >= 0 and dif_x <= 698 and dif_y >= 0 and dif_y <= 523:
            self.label.move(dif_x, dif_y)

        self.rotar(self.x_mouse, self.y_mouse, move=True)

    @property
    def x_player(self):
        return self.label.pos().x() + (self.label.width() // 2) - 13

    @property
    def y_player(self):
        return self.label.pos().y() + (self.label.height() // 2)

    def rotar(self, x_mouse_main, y_mouse_main, move):
        self.x_mouse = x_mouse_main
        self.y_mouse = y_mouse_main
        dif_x = self.x_mouse - self.x_player
        dif_y = self.y_player - self.y_mouse
        if dif_y == 0:
            dif_y = 0.00001
        norma = sqrt(dif_x**2 + dif_y**2)
        self.vector_mouse = ((dif_x / norma), (dif_y / norma))

        self.theta = degrees(atan2(dif_y, dif_x)) * -1
        self.aplicar_rotacion(self.theta, move=move)

    def disparar(self):
        if self.main.municiones != 0:
            self.main.municiones -= 1
            self.main.municion.setText(str(self.main.municiones))
            bala_label = QtGui.QLabel("", self.main.arena)
            bala_label.setMouseTracking(True)
            pos_x = self.x_player + self.vector_mouse[0] * 25
            pos_y = self.y_player - self.vector_mouse[1] * 25
            bala_label.move(pos_x, pos_y)
            pixmap = self.main.pics["bala"]
            pixmap = pixmap.scaled(self.main.pics["bala"].size(),
                                   QtCore.Qt.KeepAspectRatio,
                                   QtCore.Qt.SmoothTransformation)
            pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.theta))
            bala_label.setPixmap(pixmap)
            bala_label.show()
            bala = Bala(
                self.main.arena, self.main, bala_label, self.vector_mouse)
            self.balas.append(bala)
            bala.start()

    def aplicar_rotacion(self, theta, move):
        if not move:
            pixmap = self.current_pic
        else:
            pixmap = next(self._pics)
            self.current_pic = pixmap
        pixmap = pixmap.scaled(self.size, QtCore.Qt.KeepAspectRatio,
                               QtCore.Qt.SmoothTransformation)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(theta))
        self.cambiar_imagen(pixmap)

    def cambiar_imagen(self, imagen):
        self.label.setPixmap(imagen)
