from PyQt4 import QtCore
import time


class Reloj(QtCore.QThread):
    trigger = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.pausa = False
        self.segundos = 0

    def run(self):
        while True:
            if not self.pausa:
                time.sleep(1)
                self.segundos += 1
            else:
                time.sleep(1)
