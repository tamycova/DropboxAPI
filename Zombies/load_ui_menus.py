from PyQt4 import uic, QtCore
from ui_methods import W

inicio = uic.loadUiType("./uis/inicio.ui")
pausa = uic.loadUiType("./uis/pausa.ui")
over = uic.loadUiType("./uis/over.ui")


class Start(inicio[0], inicio[1]):

    def __init__(self, juego, pics):
        super().__init__()
        self.juego = juego
        self.setupUi(self)
        W.set_geometry(self)
        self.boton_inicio.clicked.connect(self.inicio)
        self.zombie.setPixmap(pics["zombie1"])
        self.zombie_2.setPixmap(pics["zombie2"])
        self.zombie_3.setPixmap(pics["zombie3"])

    def inicio(self):
        self.hide()
        self.juego.show()
        self.juego.run()


class Pause(pausa[0], pausa[1]):

    def __init__(self, pics):
        super().__init__()
        self.setupUi(self)
        self.juego = None
        W.set_geometry(self)
        self.zombie.setPixmap(pics["zombie1"])
        self.burbuja.setPixmap(pics["cloud"])

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.hide()
            self.juego.show()
            self.juego.restart()
            W.set_geometry(self)


class Over(over[0], over[1]):

    def __init__(self, pics):
        super().__init__()
        self.setupUi(self)
        W.set_geometry(self)
        self.zombie.setPixmap(pics["end_zombie"])
