from PyQt4 import QtGui
from sys import argv
from log_in import LogIn
from user_window import UserWindow

if __name__ == '__main__':
    app = QtGui.QApplication(argv)
    pics = {"logo": QtGui.QPixmap("./assets/logo"),
            "logo_xs": QtGui.QPixmap("./assets/logo_xs"),
            "error_code": QtGui.QPixmap("./assets/error_code"),
            "descargando": QtGui.QPixmap("./assets/descargando"),
            "folder": QtGui.QIcon(QtGui.QPixmap("./assets/folder"))}
    user_window = UserWindow(pics)
    log_in = LogIn(pics, user_window)
    log_in.show()
    app.exec_()
