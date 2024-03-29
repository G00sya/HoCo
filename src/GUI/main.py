from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *

import sys
import os
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
