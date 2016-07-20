from PyQt4 import QtCore, QtGui
from random import expovariate, randint, choice
import time
from math import sqrt, atan2, degrees
from itertools import cycle


class ZombieGenerator(QtCore.QThread):
    trigger = QtCore.pyqtSignal(object)

    def __init__(self, arena, main):
        super().__init__()
        self.trigger.connect(self.insertar_zombie)
        self.pausa = False
        self.arena = arena
        self.main = main

    @property
    def lambda_zombies(self):
        f = 4 - self.main.reloj.segundos / 30
        if f < 1:
            f = 1
        return 1 / f

    def run(self):
        while True:
            if not self.pausa:
                self.next_zombie = expovariate(self.lambda_zombies)
                self.trigger.emit(self)
                self.sleep(self.next_zombie)
            else:
                time.sleep(1)

    def insertar_zombie(self):
        zombie_label = QtGui.QLabel("", self.arena)
        zombie_label.setMouseTracking(True)
        pos_ok = False
        while not pos_ok:
            pos = choice([(0, randint(0, 523)), (698, randint(
                0, 523)), (randint(0, 698), 523), (randint(0, 698), 0)])
            distancia = sqrt((self.main.jugador.x_player - pos[0])**2
                             + (self.main.jugador.y_player - pos[1])**2)
            if distancia > 300:
                pos_ok = True
        zombie_label.move(*pos)
        zombie_label.setPixmap(self.main.pics["z6"])
        zombie_label.show()
        zombie = Zombie(self.arena, self.main, zombie_label)
        self.main.zombies_list.append(zombie)
        zombie.start()


class Zombie(QtCore.QThread):
    trigger = QtCore.pyqtSignal(object)
    trigger_attack = QtCore.pyqtSignal(object)
    trigger_atacado = QtCore.pyqtSignal(object)

    def __init__(self, arena, main, label):
        super().__init__()
        self.trigger.connect(self.mover)
        self.trigger_attack.connect(self.atacar)
        self.trigger_atacado.connect(self.morir)
        self.arena = arena
        self.main = main
        self.label = label
        self.size = self.main.pics["z1"].size()
        self.done = False

        self.pics = cycle([self.main.pics["z" + str(i)] for i in range(1, 7)])

    @property
    def centro_x(self):
        return self.label.pos().x() + self.label.width() // 2

    @property
    def centro_y(self):
        return self.label.pos().y() + self.label.height() // 2

    @property
    def distancia_player(self):
        x = self.label.pos().x() + self.label.width() // 2
        y = self.label.pos().y() + self.label.height() // 2
        d = sqrt((self.main.jugador.x_player - x)**2
                 + (self.main.jugador.y_player - y)**2)
        return d

    def run(self):
        while True and not self.done:
            if not self.main.en_pausa:
                time.sleep(0.3)
                self.trigger.emit(self)
                if self.distancia_player <= 40:
                    self.trigger_attack.emit(self)
                    time.sleep(1)
                    self.main.atacado.hide()
            else:
                time.sleep(0.1)
        self.main.update_puntaje()
        time.sleep(1)
        self.main.dead.hide()
        self.terminate()
        self.main.zombies_list.remove(self)

    def atacar(self):
        self.main.atacado.show()
        self.main.salud -= 10
        self.main.vida.setValue(self.main.salud)
        if self.main.salud == 0:
            self.main.game_over()

    def mover(self):
        try:
            x_rel = self.label.pos().x()
            y_rel = self.label.pos().y()
            x_player = self.main.jugador.x_player
            y_player = self.main.jugador.y_player
            x_propio = x_rel + (self.label.width() // 2)
            y_propio = y_rel + (self.label.height() // 2)
            dif_x = x_player - x_propio
            dif_y = y_propio - y_player
            norma = sqrt(dif_x**2 + dif_y**2)
            vector_mouse = ((dif_x / norma) * 6, (dif_y / norma) * 6)
            self.label.move(
                x_rel + vector_mouse[0] * 3, y_rel - vector_mouse[1] * 3)
            theta = degrees(atan2(dif_y, dif_x)) * -1
            self.aplicar_rotacion(theta)
        except ZeroDivisionError:
            pass

    def aplicar_rotacion(self, theta):
        pixmap = next(self.pics)
        pixmap = pixmap.scaled(self.size, QtCore.Qt.KeepAspectRatio,
                               QtCore.Qt.SmoothTransformation)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(theta))
        self.cambiar_imagen(pixmap)

    def cambiar_imagen(self, imagen):
        self.label.setPixmap(imagen)

    def morir(self):
        self.main.matados += 1
        self.main.killed.setText(str(self.main.matados))
        self.done = True
        self.label.hide()
