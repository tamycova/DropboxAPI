from PyQt4 import QtGui


class W:

    @classmethod
    def set_geometry(cls, widget):
        centro = QtGui.QDesktopWidget().availableGeometry().center()
        geom = widget.frameGeometry()
        geom.moveCenter(centro)
        widget.move(geom.topLeft())
        return widget
