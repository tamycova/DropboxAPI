from PyQt4 import uic, QtGui
from pop_ups import Historial
from tree import Arbol
from dropbox import files
import os
import shutil

user_window = uic.loadUiType("./uis/user_window.ui")


class Archivo(QtGui.QTreeWidgetItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.meta = kwargs["meta"]
        self.folder = False
        self.path = self.meta.path_lower
        self.nombre = self.meta.name
        if type(self.meta) == files.FolderMetadata:
            self.folder = True
            self.setIcon(0, kwargs["p"]["folder"])


class UserWindow(user_window[0], user_window[1]):

    def __init__(self, pics):
        super().__init__()
        self.setupUi(self)
        self.user = False
        self.pics = pics
        self.logo.setPixmap(pics["logo_xs"])
        self.TREE.itemDoubleClicked.connect(self.item_menu)
        self.moviendo = (False, None)

    def item_menu(self, obj):
        if not self.moviendo[0]:
            self.menu = QtGui.QMenu("", self)
            self.menu.move(QtGui.QCursor.pos().x(), QtGui.QCursor.pos().y())
            self.menu.addAction("Descargar", lambda: self.download(obj))
            self.menu.addAction("Historial de modificaciones",
                                lambda: self.show_meta(obj))
            self.menu.addAction("Cambiar nombre", lambda: self.rename(obj))
            self.menu.addAction("Mover", lambda: self.mover(obj))

            if obj.folder:
                self.menu.addAction(
                    "Subir archivo a esta carpeta",
                    lambda: self.upload_file(obj))
                self.menu.addAction(
                    "Crear nueva carpeta en mismo directorio",
                    lambda: self.create_new(obj))
            self.menu.show()

        else:
            if obj.folder:
                self.mover_(self.moviendo, obj)

    def file_meta(self, file_path):
        historial = self.user.files_list_revisions(
            file_path, limit=100).entries
        return historial

    def folder_meta(self, folder_path):
        historial = []
        hijos = [e.path_lower for e in self.user.files_list_folder(
            folder_path, recursive=True).entries if
            type(e) != files.FolderMetadata]
        for hijo in hijos:
            historial.extend(self.file_meta(hijo))
        return historial

    def show_meta(self, obj):
        try:
            if not obj.folder:
                historial = self.file_meta(obj.path)
            else:
                historial = self.folder_meta(obj.path)
            self.pop_up = Historial(historial, obj.nombre, self)
            self.hide()
            self.pop_up.show()
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "No se pudo acceder a historial,\
                         intente nuevamente o revise su conexion")

    def download_file(self, path, to_path):
        meta, result = self.user.files_download(path)
        byte_data = result.content
        with open(to_path, "wb") as f:
            f.write(byte_data)

    def download_folder(self, widget_item, master):
        dir_path = "./downloads{0}{1}".format(
            "/" + master.nombre, widget_item.path[len(master.path):])
        os.makedirs(dir_path)
        hijos = widget_item.childCount()
        for i in range(hijos):
            hijo = widget_item.child(i)
            data = ("/" + master.nombre + widget_item.path[len(master.path):],
                    hijo.path[len(widget_item.path):])
            path_to = "./downloads{0}{1}".format(*data)
            if not hijo.folder:
                self.download_file(hijo.path, path_to)
            else:
                self.download_folder(hijo, master)

    def download(self, obj):
        try:
            if not obj.folder:
                self.download_file(
                    obj.path, "./downloads/{}".format(obj.nombre))
            else:
                if os.path.isdir("./downloads/{}".format(obj.nombre)):
                    shutil.rmtree("./downloads/{}".format(obj.nombre))
                self.download_folder(obj, obj)
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "No se pudo realizar la descarga,\
                    intente nuevamente o revise su conexion")

    def upload_file(self, obj):
        try:
            legit_path = QtGui.QFileDialog.getOpenFileName()
            with open(legit_path, "rb") as f:
                data = f.read()
            dpx_path = obj.path + "/" + legit_path.split("/")[-1]
            self.user.files_upload(data, dpx_path, autorename=True)
            self.visualize()
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "No se pudo subir archivo,\
                    intente nuevamente o revise su conexion")

    def create_new(self, obj):
        try:
            dir_path = obj.path[:len(obj.path) - len(obj.nombre)]
            names = [e.name for e in self.user.files_list_folder(
                "", recursive=True).entries]
            i = 0
            while True:
                name = "untitled_" + str(i)
                if name in names:
                    i += 1
                else:
                    break
            self.user.files_create_folder(dir_path + name)
            self.visualize()
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "No se pudo crear directorio,\
                         intente nuevamente o revise su conexion")

    def rename(self, obj):
        try:
            name_, ok = QtGui.QInputDialog.getText(self, "Cambio de nombre " +
                                                   obj.nombre, "Nuevo nombre:")
            if ok:
                if obj.folder:
                    folders = [e.name for e in self.user.files_list_folder
                               ('', recursive=True).entries if type(e) ==
                               files.FolderMetadata]
                    if name_ in folders:
                        raise
                old_path = obj.path[:len(obj.path) - len(obj.nombre)]
                new_path = old_path + name_
                self.user.files_move(obj.path, new_path)
                self.visualize()
            else:
                pass
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "No se pudo renombrar archivo,\
                         intente nuevamente con otro nombre\
                          o revise su conexion")

    def mover(self, obj):
        self.moviendo = (True, obj)

    def mover_(self, tupla, obj):
        try:
            from_path = tupla[1].path
            to_path = obj.path + "/" + tupla[1].nombre
            self.user.files_move(from_path, to_path)
            self.moviendo = (False, None)
            self.visualize()
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "No se pudo mover,\
                         intente nuevamente con otro directorio\
                          o revise su conexion")
            self.moviendo = (False, None)

    def add_user(self, user):
        self.user = user
        self.name.setText("Hola " + self.user.users_get_current_account()
                          .email + " !")

        ok = self.check_names()
        if ok:
            self.visualize()
        else:
            msg = "Tambox no trabaja con carpetas nombradas igual.\n"
            msg += "Si quiere trabajar con Tambox debe ingresar a Dropbox y"
            msg += " asegurarse de que\n"
            msg += "no tiene dos directorios con el mismo nombre"
            QtGui.QMessageBox.information(
                self, "ERROR", msg)

    def visualize(self):
        try:
            self.TREE.clear()
            archivos = [(e.path_lower, e) for e in
                        self.user.files_list_folder('',
                                                    recursive=True).entries]
            self.arbol = Arbol(archivos)
            nivel = self.arbol.get_heads()
            primer_nivel = True
            while len(nivel) > 0:
                next_nivel = []
                for n in nivel:
                    if primer_nivel:
                        padre = (n, Archivo(self.TREE, [n.nombre],
                                            meta=n.meta, p=self.pics))
                    else:
                        padre = n
                    for hijo in padre[0].hijos:
                        child = (
                            hijo, Archivo(padre[1], [hijo.nombre],
                                          meta=hijo.meta, p=self.pics))
                        next_nivel.append(child)
                nivel = next_nivel
                primer_nivel = False
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "Visualizacion incorrecta,\
                         intente cargar Tambox nuevamente o\
                          revise su conexion")

    def check_names(self):
        try:
            folders = [e.name for e in self.user.files_list_folder
                       ('', recursive=True).entries if
                       type(e) == files.FolderMetadata]
            set_folders = set(folders)
            if len(folders) != len(set_folders):
                return False
            return True
        except:
            QtGui.QMessageBox.information(
                self, "ERROR", "Visualizacion incorrecta,\
                     intente cargar Tambox nuevamente o\
                      revise su conexion")
