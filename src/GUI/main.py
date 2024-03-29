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
        self.window_font = None
        self.init_ui()

        self.current_file = None

    def init_ui(self):
        self.setWindowTitle("HoCo code editor")
        self.resize(1300, 900)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        stylesheet_path = os.path.join(dir_path, "../../static/css/style.qss")
        self.setStyleSheet(open(stylesheet_path, "r").read())

        self.window_font = QFont("Fire Code")
        self.window_font.setPointSize(16)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()

        self.show()

    def get_editor(self) -> QsciScintilla:
        """
        Get editor to a tab

        :return:
        """

    def set_up_menu(self):
        """

        :return:
        """
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")

        new_file = file_menu.addAction("New")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)

    def new_file(self):
        pass

    def open_file(self):
        pass

    def open_folder(self):
        pass

    def set_up_body(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
