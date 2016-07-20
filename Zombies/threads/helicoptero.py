from PyQt4 import QtCore, QtGui
from random import randint
from math import sqrt
import time


class Helicoptero(QtCore.QThread):
    trigger = QtCore.pyqtSignal(object)

    def __init__(self, arena, main):
        super().__init__()
        self.trigger.connect(self.insertar_regalitos)
        self.pausa = False
        self.arena = arena
        self.main = main

    def run(self):
        self.sleep(30)
        while True:
            if not self.pausa:
                self.trigger.emit(self)
                self.sleep(30)
            else:
                time.sleep(1)

    def insertar_regalitos(self):
        posiciones = self.get_positions()
        municion_label = QtGui.QLabel("", self.arena)
        vida_label = QtGui.QLabel("", self.arena)
        municion_label.setMouseTracking(True)
        vida_label.setMouseTracking(True)
        municion_label.move(*posiciones[0])
        vida_label.move(*posiciones[1])
        municion_label.setPixmap(self.main.pics["municiones"])
        vida_label.setPixmap(self.main.pics["vida"])
        municion_label.show()
        vida_label.show()
        municion = Regalo(self.arena, self.main, municion_label, "municiones")
        vida = Regalo(self.arena, self.main, vida_label, "vida")
        self.main.regalos_list.extend([municion, vida])
        municion.start()
        vida.start()

    def get_positions(self):
        pos = []
        while len(pos) < 2:
            x = randint(0, 698)
            y = randint(0, 523)
            distancia = sqrt((self.main.jugador.x_player - x)**2
                             + (self.main.jugador.y_player - y)**2)
            if distancia > 300:
                pos.append((x, y))
        return pos


class Regalo(QtCore.QThread):
    trigger_found = QtCore.pyqtSignal(object)
    trigger_end = QtCore.pyqtSignal(object)

    def __init__(self, arena, main, label, tipo):
        super().__init__()
        self.trigger_found.connect(self.found)
        self.trigger_end.connect(self.end)
        self.arena = arena
        self.main = main
        self.label = label
        self.tipo = tipo
        self.contador = 0
        self.x = self.label.pos().x() + self.label.width() // 2
        self.y = self.label.pos().y() + self.label.height() // 2

    @property
    def distancia_player(self):
        d = sqrt((self.main.jugador.x_player - self.x)**2
                 + (self.main.jugador.y_player - self.y)**2)
        return d

    def run(self):
        while True:
            if not self.main.en_pausa:
                time.sleep(0.1)
                self.contador += 1
                if self.contador == 150:
                    self.trigger_end.emit(self)
                elif self.distancia_player <= 40:
                    self.trigger_found.emit(self)
            else:
                time.sleep(1)

    def found(self):
        self.label.hide()
        if self.tipo == "municiones":
            self.main.municiones += 30
            self.main.municion.setText(str(self.main.municiones))
        else:
            self.main.salud += 20
            if self.main.salud <= 100:
                self.main.vida.setValue(self.main.salud)
            else:
                self.main.salud = 100
                self.main.vida.setValue(self.main.salud)
        self.terminate()
        self.main.regalos_list.remove(self)

    def end(self):
        self.label.hide()
        self.terminate()
        self.main.regalos_list.remove(self)

