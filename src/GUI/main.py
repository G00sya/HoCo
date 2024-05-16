from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *

import os
from pathlib import Path

from editor import Editor
from file_manager import FileManager
from Parser import *
from Scanner import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # add before init
        self.vcc_path = None
        self.tree_root = None
        self.current_editor = None
        self.side_bar_clr = "#282c34"
        self.current_style = None

        self.init_ui()

        self.current_file = None
        self.current_side_bar = None

    def init_ui(self):
        self.app_name = "PYQT EDITOR"
        self.setWindowTitle(self.app_name)
        self.resize(1300, 900)

        root_dir = os.getcwd()
        full_path = os.path.join("static", "css", "style.qss")
        absolute_path = os.path.join(root_dir, full_path)

        self.setStyleSheet(open(absolute_path, "r").read())

        # alternative Consolas font
        self.window_font = QFont(
            "Fire Code")  # font needs to be installed in your computer if its not use something else
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()
        self.set_up_status_bar()

        self.show()

    def set_up_status_bar(self):
        # Create status bar
        stat = QStatusBar(self)
        stat.setStyleSheet("color: #D3D3D3;")
        stat.showMessage("Ready", 3000)
        self.setStatusBar(stat)

    def set_up_menu(self):
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

        file_menu.addSeparator()

        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)

        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")

        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)

        # Style menu
        style_menu = menu_bar.addMenu("Backlight style")
        style_action1 = style_menu.addAction("Set style 1")
        style_action2 = style_menu.addAction("Set style 2")
        style_action3 = style_menu.addAction("Set style 3")
        style_action1.triggered.connect(self.set_style1)
        style_action2.triggered.connect(self.set_style2)
        style_action3.triggered.connect(self.set_style3)
        # you can add more


    def get_editor(self, path: Path = None, is_python_file=False, is_VeKrestKrest_file = True) -> QsciScintilla:
        if is_VeKrestKrest_file:
            editor = Editor(self, path=path, is_python_file=False, is_VeKrestKrest_file=True)
        elif is_python_file:
            editor = Editor(self, path=path, is_python_file=True, is_VeKrestKrest_file=False)
        else:
            editor = Editor(self, path=path, is_python_file=False, is_VeKrestKrest_file=False)
        return editor

    def is_binary(self, path):
        '''
        Check if file is binary
        '''
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)

    def set_new_tab(self, path: Path, is_new_file=False):
        if not is_new_file and self.is_binary(path):
            self.statusBar().showMessage("Cannot Open Binary File", 2000)
            return

        if path.is_dir():
            return

        # add whichever extentions you consider as programming language file
        editor = self.get_editor(path, path.suffix in {".py", ".pyw"}, path.suffix == ".vcc")

        if is_new_file:
            self.tab_view.addTab(editor, "untitled")
            self.setWindowTitle("untitled - " + self.app_name)
            self.statusBar().showMessage("Opened untitled")
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return

        # check if file already open
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name or self.tab_view.tabText(i) == "*" + path.name:
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return

        # create new tab
        self.tab_view.addTab(editor, path.name)
        editor.setText(path.read_text(encoding="utf-8"))
        if path.suffix == ".vcc":
            self.current_editor = editor
            self.build_ast(self.current_editor)
        self.setWindowTitle(f"{path.name} - {self.app_name}")
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage(f"Opened {path.name}", 2000)

    def set_cursor_pointer(self, e):
        self.setCursor(Qt.PointingHandCursor)

    def set_cursor_arrow(self, e):
        self.setCursor(Qt.ArrowCursor)

    def get_side_bar_label(self, path, name):
        label = QLabel()
        label.setPixmap(QPixmap(path).scaled(QSize(30, 30)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_tab(e, name)
        # Chaning Cursor on hover
        label.enterEvent = self.set_cursor_pointer
        label.leaveEvent = self.set_cursor_arrow
        return label

    def get_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Plain)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setStyleSheet('''
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
            }
            QFrame:hover {
                color: white;
            }
        ''')
        return frame

    def build_ast(self, editor):
        def clear_widget(tree_widget):
            tree_widget.clear()

        def fill_widget(tree_widget, node, depth=0):
            item = QTreeWidgetItem(tree_widget)
            item.setText(0, node.value)
            item.setData(0, Qt.UserRole, node)

            for child_node in node.childs:
                fill_widget(item, child_node, depth + 1)

            item.setExpanded(True)

        code = editor.text()
        scanner = Scanner(code)
        parser = Parser()
        ast_tree_code = parser.Parse(scanner)
        self.tree_root = ast_tree_code.GetRoot()

        clear_widget(self.ast_tree)

        fill_widget(self.ast_tree, self.tree_root, 0)

    def set_up_body(self):

        # Body
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

        ##############################
        ###### TAB VIEW ##########

        # Tab Widget to add editor to
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)

        ##############################
        ###### SIDE BAR ##########
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setStyleSheet(f'''
            background-color: {self.side_bar_clr};
        ''')
        side_bar_layout = QVBoxLayout()
        side_bar_layout.setContentsMargins(5, 10, 5, 0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)


        root_dir = os.getcwd()
        full_path = os.path.join("static", "icons", "folder-icon-blue.svg")
        absolute_path = os.path.join(root_dir, full_path)

        folder_label = self.get_side_bar_label(absolute_path, "folder-icon")
        side_bar_layout.addWidget(folder_label)

        self.side_bar.setLayout(side_bar_layout)

        # split view
        self.hsplit = QSplitter(Qt.Horizontal)

        ##############################
        ###### FILE MANAGER ##########

        # frame and layout to hold tree view (file manager)
        self.file_manager_frame = self.get_frame()
        self.file_manager_frame.setMaximumWidth(400)
        self.file_manager_frame.setMinimumWidth(200)

        self.file_manager_layout = QVBoxLayout()
        self.file_manager_layout.setContentsMargins(0, 0, 0, 0)
        self.file_manager_layout.setSpacing(0)

        self.file_manager = FileManager(  # Check
            tab_view=self.tab_view,
            set_new_tab=self.set_new_tab,
            main_window=self
        )

        # setup layout
        self.file_manager_layout.addWidget(self.file_manager)
        self.file_manager_frame.setLayout(self.file_manager_layout)

        # create ast
        self.ast_tree = QTreeWidget()
        self.ast_tree.setFrameShape(QFrame.StyledPanel)
        self.ast_tree.setFrameShadow(QFrame.Plain)
        self.ast_tree.setStyleSheet(f'''
                          background-color: {self.side_bar_clr};
                          color: #30d5c8;
                          font: 12pt 'Fire Code'; 
                          font-weight: bold;
                      ''')

        # configuring the header
        self.ast_tree.setHeaderLabel("Ast tree")


        def on_ast_node_selected(item):
            node = item.data(0, Qt.UserRole)
            start_line, start_index = self.current_editor.lineIndexFromPosition(node.start_pos + 1)
            end_line, end_index = self.current_editor.lineIndexFromPosition(node.end_pos + 1)

            self.current_editor.setSelection(start_line, start_index, end_line, end_index)

        self.ast_tree.itemClicked.connect(lambda item: on_ast_node_selected(item))

        ##############################
        ###### SETUP WIDGETS ##########

        # add tree view and tab view
        self.hsplit.addWidget(self.file_manager_frame)
        self.hsplit.addWidget(self.tab_view)
        self.hsplit.addWidget(self.ast_tree)

        body.addWidget(self.side_bar)
        body.addWidget(self.hsplit)

        body_frame.setLayout(body)

        self.setCentralWidget(body_frame)

    def show_dialog(self, title, msg) -> int:
        dialog = QMessageBox(self)
        dialog.setFont(self.font())
        dialog.font().setPointSize(14)
        dialog.setWindowTitle(title)
        dialog.setWindowIcon(QIcon(":/icons/close-icon.svg"))
        dialog.setText(msg)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        dialog.setIcon(QMessageBox.Warning)
        return dialog.exec_()

    def close_tab(self, index):
        editor: Editor = self.tab_view.currentWidget()
        if editor.current_file_changed:
            dialog = self.show_dialog(
                "Close", f"Do you want to save the changes made to {self.current_file.name}?"
            )
            if dialog == QMessageBox.Yes:
                self.save_file()

        self.ast_tree.clear()
        self.tab_view.removeTab(index)

    def show_hide_tab(self, e, type_):
        if type_ == "folder-icon":
            if not (self.file_manager_frame in self.hsplit.children()):
                self.hsplit.replaceWidget(0, self.file_manager_frame)
        elif type_ == "search-icon":
            if not (self.search_frame in self.hsplit.children()):
                self.hsplit.replaceWidget(0, self.search_frame)

        if self.current_side_bar == type_:
            frame = self.hsplit.children()[0]
            if frame.isHidden():
                frame.show()
            else:
                frame.hide()

        self.current_side_bar = type_

    def tree_view_context_menu(self, pos):
        ...

    def new_file(self):
        self.set_new_tab(Path("untitled"), is_new_file=True)

    def save_file(self):
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()

        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.build_ast(editor)
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)
        editor.current_file_changed = False

    def save_as(self):
        # save as
        editor = self.tab_view.currentWidget()
        if editor is None:
            return

        file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return

        path = Path(file_path)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)
        self.current_file = path
        editor.current_file_changed = False

    def open_file(self):
        # open file
        ops = QFileDialog.Options()  # this is optional
        ops |= QFileDialog.DontUseNativeDialog
        # I will add support for opening multiple files later for now it can only open one at a time
        new_file, _ = QFileDialog.getOpenFileName(self,
                                                  "Pick A File", "", "All Files (*);;Python Files (*.py)",
                                                  options=ops)
        if new_file == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return
        f = Path(new_file)
        self.set_new_tab(f)

    def open_folder(self):
        # open folder
        ops = QFileDialog.Options()  # this is optional
        ops |= QFileDialog.DontUseNativeDialog

        new_folder = QFileDialog.getExistingDirectory(self, "Pick A Folder", "", options=ops)
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)

    def copy(self):
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.copy()

    def set_style1(self, style_type):
        self.current_style = os.getcwd() + "\\..\\..\\static\\theme.json"
        if self.current_editor.is_VeKrestKrest_file:
            self.current_editor.VeKrestKrestlexer.theme = self.current_style

    def set_style2(self, style_type):
        self.current_style = os.getcwd() + "\\..\\..\\static\\theme.json"
        if self.current_editor.is_VeKrestKrest_file:
            self.current_editor.VeKrestKrestlexer.theme = self.current_style

    def set_style3(self, style_type):
        self.current_style = os.getcwd() + "\\..\\..\\static\\theme.json"
        if self.current_editor.is_VeKrestKrest_file:
            self.current_editor.VeKrestKrestlexer.theme = self.current_style


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
