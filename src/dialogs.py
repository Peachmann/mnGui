from PyQt6.QtWidgets import QDialog, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from ui.ui_add_host_dialog import Ui_Dialog as AddHostDialogUi
from ui.ui_add_switch_dialog import Ui_Dialog as AddSwitchDialogUi


class AddHostDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddHostDialogUi()
        self.ui.setupUi(self)

    def populate_switch_list(self, values):
        self.ui.switch_box.addItems(['s1', 's2'])

class AddSwitchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddSwitchDialogUi()
        self.ui.setupUi(self)

    def populate_switch_multi_select(self, switches):
        for switch in switches:
            item = QListWidgetItem(switch)
            self.ui.switch_list.addItem(item)