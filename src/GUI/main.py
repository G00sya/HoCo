from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import os
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.side_bar_clr = "#282c34"
        self.init_ui()

        self.window_font = None
        self.current_file = None

        self.sidebar_frame = None
        self.tree_frame = None

    def init_ui(self):
        self.setWindowTitle("HoCo code editor")
        self.resize(1300, 900)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        stylesheet_path = os.path.join(dir_path, "../../static/css/style.qss")
        self.setStyleSheet(open(stylesheet_path, "r").read())

        self.window_font = QFont("Fire Code")  # must be installed
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
# Menu -----------------------------------------------------------------------------------------------------------------
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

# Body -----------------------------------------------------------------------------------------------------------------
    def set_up_body(self):
        """

        :return:
        """
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        # Sidebar frame ------------------------------------------------------------------------------------------------------
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFrameShape(QFrame.StyledPanel)
        self.sidebar_frame.setFrameShadow(QFrame.Plain)
        self.sidebar_frame.setStyleSheet(f'''
                    background-color: {self.side_bar_clr};
                ''')
        sidebar_frame_layout = QHBoxLayout()
        sidebar_frame_layout.setContentsMargins(5, 10, 5, 0)
        sidebar_frame_layout.setSpacing(0)
        sidebar_frame_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.sidebar_frame.setLayout(sidebar_frame_layout)

        body.addWidget(self.sidebar_frame)
        self.hsplit = QSplitter(Qt.Horizontal)

        # File manager frame -------------------------------------------------------------------------------------------
        self.tree_frame = QFrame()
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(400)
        self.tree_frame.setMinimumWidth(200)
        self.tree_frame.setBaseSize(100, 0)
        self.tree_frame.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout = QVBoxLayout()
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout.setSpacing(0)
        self.tree_frame.setStyleSheet('''
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
            }
            QFrame: hover {
                color: white;
            }
        ''')


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
