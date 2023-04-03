from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic
import sys


class UI(QWidget):
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)
        uic.loadUi("main.ui", self)


app = QApplication(sys.argv)
window = UI()
window.show()
sys.exit(app.exec())
