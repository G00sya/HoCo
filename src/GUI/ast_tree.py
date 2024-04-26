import ast
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

def fill_item(item, value):
    item.setExpanded(True)
    if isinstance(value, dict):
        for key, val in value.items():
            child = QTreeWidgetItem()
            child.setText(0, str(key))
            item.addChild(child)
            if isinstance(val, (dict, list)):
                fill_item(child, val)
            else:
                child.setText(1, str(val))
    elif isinstance(value, list):
        for val in value:
            child = QTreeWidgetItem()
            item.addChild(child)
            if isinstance(val, (dict, list)):
                fill_item(child, val)
            else:
                child.setText(0, str(val))
    else:
        child = QTreeWidgetItem()
        child.setText(0, str(value))
        item.addChild(child)

def fill_widget(widget, value):
    widget.clear()
    fill_item(widget.invisibleRootItem(), value)
