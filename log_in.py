from PyQt4 import uic, QtCore, QtWebKit, QtGui
from dropbox import DropboxOAuth2FlowNoRedirect, Dropbox

APP_KEY = ""  # INSERT YOUR APP_KEY
APP_SECRET = ""  # INSERT YOUR APP_SECRET
log_in = uic.loadUiType("./uis/log_in.ui")


class WebView(QtWebKit.QWebView):

    def closeEvent(self, event):
        self.parent.show()


class LogIn(log_in[0], log_in[1]):

    def __init__(self, pics, user_window):
        super().__init__()
        self.setupUi(self)
        self.pics = pics
        self.logo.setPixmap(pics["logo"])
        self.conectar.clicked.connect(self.log_in)
        self.ingresar.clicked.connect(self.access)
        self.auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        self.user_window = user_window

    def log_in(self):
        try:
            self.logo.setPixmap(self.pics["logo"])
            self.autorizo = True
            url = self.auth_flow.start()
            self.web_view = WebView()
            self.web_view.parent = self
            self.web_view.setWindowTitle("Obteniendo codigo para TamBox")
            self.web_view.load(QtCore.QUrl(url))
            self.hide()
            self.web_view.show()
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "No se pudo conectar a Dropbox,\
                                revise su conexion")

    def access(self):
        self.logo.setPixmap(self.pics["logo"])
        code = self.token.text()
        try:
            token, user = self.auth_flow.finish(code)
            self.dbx = Dropbox(token)
            self.continuar()

        except:
            self.logo.setPixmap(self.pics["error_code"])
            QtGui.QMessageBox.information(
                self, "ERROR", "Codigo invalido,\
                         intente nuevamente o revise su conexion")

    def continuar(self):
        self.hide()
        self.user_window.add_user(self.dbx)
        self.user_window.show()
