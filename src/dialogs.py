from PyQt6.QtWidgets import QDialog, QListWidgetItem
from ui.ui_add_host_dialog import Ui_Dialog as AddHostDialogUi
from ui.ui_add_switch_dialog import Ui_Dialog as AddSwitchDialogUi
from ui.ui_remove_host_dialog import Ui_Dialog as RemoveHostDialogUi


class AddHostDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddHostDialogUi()
        self.ui.setupUi(self)
        self.ui.auto_name.stateChanged.connect(self.update_host_name_field)
        self.mac = 0


    def init_selections(self, switches, ids):
        for switch in switches:
            self.ui.switch_box.addItem(switch['name'])
        
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

class RemoveHostDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = RemoveHostDialogUi()
        self.ui.setupUi(self)
        self.host_and_mac_dict = {}
    
    def init_hosts_and_macs(self, hosts):
        for host in hosts:
            self.ui.host_box.addItem(host['name'])
            self.host_and_mac_dict[host['name']] = host['mac']
        self.ui.host_box.currentTextChanged.connect(self.update_mac)
        self.update_mac()

    def update_mac(self):
        selected_host = self.ui.host_box.currentText()
        self.ui.mac_name.setText(self.host_and_mac_dict[selected_host])


class AddSwitchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddSwitchDialogUi()
        self.ui.setupUi(self)
        self.dpid = 0

    def init_selections(self, switches, ids):
        for switch in switches:
            self.ui.switch_list.addItem(QListWidgetItem(switch['name']))
        
        self.dpid = ids['dpid']
        self.ui.dpid_name.setText(str(self.dpid))
        self.update_switch_name_field()
        self.ui.auto_name.stateChanged.connect(self.update_switch_name_field)

    def update_switch_name_field(self):
        if self.ui.auto_name.isChecked():
            self.ui.switch_name.setEnabled(False)
            self.ui.switch_name.setText(f"s{self.dpid}")
        else:
            self.ui.switch_name.setEnabled(True)
            self.ui.switch_name.clear()

class RemoveSwitchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)