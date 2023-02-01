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
        self.ui.auto_name.stateChanged.connect(self.update_host_name_field)
        self.mac = 0


    def init_selections(self, switches, ids):
        for s in switches:
            self.ui.switch_box.addItem(s['name'])
        
        self.mac = ids['mac']
        if self.mac < 10:
            self.mac = f"0{ids['mac']}" 
            
        self.ui.mac_name.setText(f"00:00:00:00:00:{self.mac}")
        self.update_host_name_field()

    def update_host_name_field(self):
        if self.ui.auto_name.isChecked():
            self.ui.host_name.setEnabled(False)
            self.ui.host_name.setText(f"h{self.mac}")
        else:
            self.ui.host_name.setEnabled(True)
            self.ui.host_name.clear()

class AddSwitchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddSwitchDialogUi()
        self.ui.setupUi(self)

    def populate_switch_multi_select(self, switches):
        for switch in switches:
            item = QListWidgetItem(switch)
            self.ui.switch_list.addItem(item)