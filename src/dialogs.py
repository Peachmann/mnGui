from PyQt6.QtWidgets import QDialog
from ui.ui_add_host_dialog import Ui_Dialog


class AddHostDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def populate_switch_list(self, values):
        self.ui.switch_box.addItems(['s1', 's2'])