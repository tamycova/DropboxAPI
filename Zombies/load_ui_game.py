from PyQt4 import uic, QtCore
from ui_methods import W
from threads.reloj import Reloj
from threads.sniper import Sniper
from threads.zombies import ZombieGenerator
from threads.helicoptero import Helicoptero

juego = uic.loadUiType("./uis/juego.ui")
direcciones = {QtCore.Qt.Key_Left: "L", QtCore.Qt.Key_Up: "U",
               QtCore.Qt.Key_Right: "R", QtCore.Qt.Key_Down: "D"}


class ZombieGame(juego[0], juego[1]):

    def __init__(self, end, pausa, pics):
        super().__init__()
        self.setupUi(self)
        self.pausa = pausa
        self.end = end
        self.pausa.juego = self
        W.set_geometry(self)

        self.en_pausa = False

        self.atacado.hide()
        self.atacado.setPixmap(pics["atacado"])
        self.dead.hide()
        self.dead.setPixmap(pics["dead"])

        self.pics = pics

        self.reloj = Reloj()
        self.jugador = Sniper(self, self.jugador)
        self.zombies = ZombieGenerator(self.arena, self)
        self.helicoptero = Helicoptero(self.arena, self)

        self.zombies_list = []
        self.regalos_list = []

        self.municiones = 20
        self.salud = 100
        self.matados = 0
        self.puntaje_ = 0

    def update_puntaje(self):
        self.puntaje_ += 2 * self.reloj.segundos
        self.puntaje.setText(str(self.puntaje_))

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Space:
            self.pausar()
        elif key in direcciones:
            self.jugador.mover(direcciones[key])

    def mouseMoveEvent(self, QMouseEvent):
        x = QMouseEvent.x()
        y = QMouseEvent.y() - 80
        if x > 0 and y > 0:
            self.jugador.rotar(x, y, move=False)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.jugador.disparar()

    def run(self):
        self.reloj.start()
        self.zombies.start()
        self.helicoptero.start()

    def restart(self):
        self.reloj.pausa = not self.reloj.pausa
        self.zombies.pausa = not self.zombies.pausa
        self.helicoptero.pausa = not self.helicoptero.pausa
        self.en_pausa = not self.en_pausa

    def pausar(self):
        self.en_pausa = not self.en_pausa
        self.reloj.pausa = not self.reloj.pausa
        self.zombies.pausa = not self.zombies.pausa
        self.helicoptero.pausa = not self.helicoptero.pausa
        self.hide()
        self.pausa.show()
        W.set_geometry(self)

    def game_over(self):
        self.hide()
        self.reloj.terminate()
        self.zombies.terminate()
        self.helicoptero.terminate()
        for z in [z for z in self.zombies_list if z.isRunning()]:
            z.terminate()
        for r in [r for r in self.regalos_list if r.isRunning()]:
            r.terminate()
        for b in [b for b in self.jugador.balas if b.isRunning()]:
            b.terminate()
        self.end.puntaje.setText(str(self.puntaje_))
        self.end.show()
