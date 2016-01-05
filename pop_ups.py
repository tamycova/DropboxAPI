from PyQt4 import uic, QtGui

historial = uic.loadUiType("./uis/historial.ui")


class Historial(historial[0], historial[1]):

    def __init__(self, historial, nombre, main):
        super().__init__()
        self.setupUi(self)
        self.hist = historial
        self.main = main
        self.ok.clicked.connect(self.cerrar)
        self.setWindowTitle("Historial de modificaciones {}".format(nombre))
        self.tabla.setRowCount(len(historial))
        n = 0
        for entry in historial[::-1]:
            n += 1
            name = QtGui.QTableWidgetItem(entry.name)
            user = QtGui.QTableWidgetItem(str(entry.client_modified))
            server = QtGui.QTableWidgetItem(str(entry.server_modified))
            self.tabla.setItem(n - 1, 0, name)
            self.tabla.setItem(n - 1, 1, user)
            self.tabla.setItem(n - 1, 2, server)

    def cerrar(self):
        self.hide()
        self.main.show()

    def closeEvent(self, event):
        self.main.show()
