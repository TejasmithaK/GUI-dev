import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, QMimeData, QByteArray, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QIcon


class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

    def startDrag(self, dropActions):
        item = self.currentItem()
        if item is None:
            return

        mime_data = QMimeData()
        mime_type = "application/x-qabstractitemmodeldatalist"

        item_text_bytes = item.text().encode('utf-8')
        mime_data.setData(mime_type, QByteArray(item_text_bytes))

        mime_data.setText(item.text())

        drag = QDrag(self)
        drag.setMimeData(mime_data)

        if item.data(Qt.ItemDataRole.DecorationRole):
            pixmap = item.data(Qt.ItemDataRole.DecorationRole).pixmap() if isinstance(item.data(
                Qt.ItemDataRole.DecorationRole), QIcon) else item.data(Qt.ItemDataRole.DecorationRole)
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
        else:
            drag.setPixmap(QPixmap())

        result = drag.exec_(dropActions, Qt.DropAction.MoveAction)

        if result == Qt.DropAction.MoveAction:
            self.takeItem(self.row(item))


class DroppableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            item_data_bytes = event.mimeData().data(
                "application/x-qabstractitemmodeldatalist").data()
            item_text = item_data_bytes.decode('utf-8')

            self.addItem(item_text)

            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()


class ItemSorterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Item Sorter with Drag & Drop (PyQt5)")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.init_ui()

    def init_ui(self):
        source_layout = QVBoxLayout()
        source_label = QLabel("<h2>Available files</h2>")
        self.source_list = DraggableListWidget()
        initial_items = ["assgn.py", "Helper.py", "Unit Test reports",
                         "Automation test results", "module_test.py", "work.log", "data.sql"]
        for item in initial_items:
            self.source_list.addItem(item)
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_list)
        self.main_layout.addLayout(source_layout)

        dest1_layout = QVBoxLayout()
        dest1_label = QLabel("<h2>Developer files</h2>")
        self.dest_list1 = DroppableListWidget()
        dest1_layout.addWidget(dest1_label)
        dest1_layout.addWidget(self.dest_list1)
        self.main_layout.addLayout(dest1_layout)

        dest2_layout = QVBoxLayout()
        dest2_label = QLabel("<h2>Testing files</h2>")
        self.dest_list2 = DroppableListWidget()
        dest2_layout.addWidget(dest2_label)
        dest2_layout.addWidget(self.dest_list2)
        self.main_layout.addLayout(dest2_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemSorterApp()
    window.show()
    sys.exit(app.exec_())
