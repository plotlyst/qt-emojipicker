import sys

from qtpy.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout

import qtemoji


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        print(next(iter(qtemoji.EMOJI_DATA.items())))

        self.widget.setLayout(QVBoxLayout())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()
