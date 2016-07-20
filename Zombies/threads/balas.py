from PyQt4 import QtCore
import time
from math import sqrt


class Bala(QtCore.QThread):
    trigger = QtCore.pyqtSignal(object)

    def __init__(self, arena, main, label, vector):
        super().__init__()
        self.trigger.connect(self.mover)
        self.arena = arena
        self.main = main
        self.label = label
        self.vector = vector
        self.recorrido = 0
        self.objetivo = None

    def run(self):
        while True:
            if not self.main.en_pausa:
                time.sleep(0.1)
                self.trigger.emit(self)
            else:
                time.sleep(0.1)

    def ataca_zombie(self):
        x = self.label.pos().x()
        y = self.label.pos().y()
        if len(self.main.zombies_list) != 0:
            z = min(self.main.zombies_list, key=lambda f: sqrt(
                (f.centro_x - x)**2 + (f.centro_y - y)**2))
            d = sqrt((z.centro_x - x)**2 + (z.centro_y - y)**2)
            if d <= 45 and not z.done:
                self.objetivo = z
                return True
        return False

    def mover(self):
        self.recorrido += sqrt(self.vector[0]**2 + self.vector[1]**2) * 10
        if self.recorrido <= 300:
            self.label.move(self.label.pos().x() + self.vector[0] * 10,
                            self.label.pos().y() - self.vector[1] * 10)
            if self.label.pos().x() < 0 or self.label.pos().y() < 0:
                self.label.hide()
                self.terminate()
                self.main.jugador.balas.remove(self)
            if self.ataca_zombie():
                self.main.dead.show()
                self.objetivo.trigger_atacado.emit(self.objetivo)
                self.label.hide()
                self.terminate()
                self.main.jugador.balas.remove(self)
        else:
            self.label.hide()
            self.terminate()
            self.main.jugador.balas.remove(self)
