from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
import operator

class TableModel(QAbstractTableModel):
    def __init__(self, parent, myList, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.myList = myList
        self.header = header

    def rowCount(self, parent):
        return len(self.myList)

    def columnCount(self, parent):
        if self.myList:
            return len(self.myList[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.myList[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()

    def sort(self, col, order):
        """Sort table by the given column number col"""
        self.layoutAboutToBeChanged.emit()
        self.myList = sorted(self.myList, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.myList.reverse()
        self.layoutChanged.emit()

    def clearTable(self):
        self.beginResetModel()
        self.myList = []
        self.endResetModel()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
