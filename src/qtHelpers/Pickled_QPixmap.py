from PyQt5 import QtCore, QtGui

"""
Substitute for QPixamp that can be pickled for saving/loading
Convert between this and QPixmap as needed
"""


class Pickled_QPixmap(QtGui.QPixmap):
    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getstate__(self):
        ba = QtCore.QByteArray()
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.WriteOnly)
        stream << self
        return ba

    def __setstate__(self, ba):
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.ReadOnly)
        stream >> self
