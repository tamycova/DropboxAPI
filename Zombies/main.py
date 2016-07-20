import sys
from PyQt4 import QtGui
from load_ui_menus import Start, Pause, Over
from load_ui_game import ZombieGame


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    pics = {"atacado": QtGui.QPixmap("./assets/sangre"),
            "p1": QtGui.QPixmap("./assets/p1"),
            "p2": QtGui.QPixmap("./assets/p2"),
            "p3": QtGui.QPixmap("./assets/p3"),
            "p4": QtGui.QPixmap("./assets/p4"),
            "zombie1": QtGui.QPixmap("./assets/inicio_zombie"),
            "zombie2": QtGui.QPixmap("./assets/inicio_zombie1"),
            "zombie3": QtGui.QPixmap("./assets/inicio_zombie2"),
            "cloud": QtGui.QPixmap("./assets/text_cloud"),
            "z1": QtGui.QPixmap("./assets/z1"),
            "z2": QtGui.QPixmap("./assets/z2"),
            "z3": QtGui.QPixmap("./assets/z3"),
            "z4": QtGui.QPixmap("./assets/z4"),
            "z5": QtGui.QPixmap("./assets/z5"),
            "z6": QtGui.QPixmap("./assets/z6"),
            "bala": QtGui.QPixmap("./assets/bullet"),
            "municiones": QtGui.QPixmap("./assets/municiones"),
            "vida":  QtGui.QPixmap("./assets/vida"),
            "dead": QtGui.QPixmap("./assets/dead"),
            "end_zombie": QtGui.QPixmap("./assets/end_zombie")}
    end = Over(pics)
    pausa = Pause(pics)
    juego = ZombieGame(end, pausa, pics)
    start = Start(juego, pics)
    start.show()
    app.exec_()
