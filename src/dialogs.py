from PyQt6.QtWidgets import QDialog, QListWidgetItem
from ui.ui_add_host_dialog import Ui_Dialog as AddHostDialogUi
from ui.ui_add_switch_dialog import Ui_Dialog as AddSwitchDialogUi
from ui.ui_remove_host_dialog import Ui_Dialog as RemoveHostDialogUi
from ui.ui_remove_switch_dialog import Ui_Dialog as RemoveSwitchDialogUi
from ui.ui_send_requests_dialog import Ui_Dialog as SendRequestDialogUi
from ui.ui_manage_flows_dialog import Ui_Dialog as ManageFlowsDialogUi
from PyQt6.QtCore import pyqtSignal, pyqtSlot

class AddHostDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddHostDialogUi()
        self.ui.setupUi(self)
        self.ui.auto_name.stateChanged.connect(self.update_host_name_field)
        self.ui.type_box.currentTextChanged.connect(self.toggle_connect_box)
        self.mac = 0


    def init_selections(self, switches, ids, hosts, host_info):
        for switch in switches:
            self.ui.switch_box.addItem(switch['name'])
        
        self.mac = ids['mac']
        if self.mac < 10:
            self.mac = f"0{ids['mac']}" 

        for host in hosts:
            if host_info[host['mac']]['host_type'] == 'Server':
                self.ui.other_host_list.addItem(QListWidgetItem(host['name']))
            
        self.ui.mac_name.setText(f"00:00:00:00:00:{self.mac}")
        self.update_host_name_field()
        self.toggle_connect_box()

    def update_host_name_field(self):
        if self.ui.auto_name.isChecked():
            self.ui.host_name.setEnabled(False)
            self.ui.host_name.setText(f"h{self.mac}")
        else:
            self.ui.host_name.setEnabled(True)
            self.ui.host_name.clear()
    
    def toggle_connect_box(self):
        if self.ui.type_box.currentText() == 'Client':
            self.ui.other_host_list.setEnabled(True)
        else:
            self.ui.other_host_list.clearSelection()
            self.ui.other_host_list.setEnabled(False)

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

class ManageFlowsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ManageFlowsDialogUi()
        self.ui.setupUi(self)
    
    def init_selections(self, hosts, host_info):
        for host in hosts:
            mac = host['mac']

            if host_info[mac]['host_type'] == 'Server':
                self.ui.server_box.addItem(host['name'])
            else:
                self.ui.client_box.addItem(host['name'])

    def modify_flows(self):
        return

class SendRequestDialog(QDialog):

    send_request_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = SendRequestDialogUi()
        self.ui.setupUi(self)
        self.name_to_ip = {}

    def init_selections(self, hosts, host_info):
        for host in hosts:
            mac = host['mac']

            if host_info[mac]['host_type'] == 'Server':
                self.ui.server_box.addItem(host['name'])
                self.name_to_ip[host['name']] = host_info[mac]['ip']
            else:
                self.ui.client_box.addItem(host['name'])

        self.ui.send_btn.clicked.connect(self.send_request)
        self.ui.hash_box.textChanged.connect(self.toggle_button)

    def toggle_button(self):
        if len(self.ui.hash_box.text()) > 0:
            self.ui.send_btn.setEnabled(True)
        else:
            self.ui.send_btn.setEnabled(False)

    def send_request(self):
        request = {'client': self.ui.client_box.currentText(),
                    'server': self.name_to_ip[self.ui.server_box.currentText()],
                    'to_hash': self.ui.hash_box.text()
            }
        self.send_request_signal.emit(request)

    @pyqtSlot(str)
    def update_response(self, response):
        self.ui.response_box.setText(response)

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
        self.ui = RemoveSwitchDialogUi()
        self.ui.setupUi(self)
        self.swtich_and_dpid_dict = {}

    def init_ui(self, switches):
        for switch in switches:
            self.ui.switch_box.addItem(switch['name'])
            self.swtich_and_dpid_dict[switch['name']] = switch['dpid']

        self.ui.switch_box.currentTextChanged.connect(self.update_dpid)
        self.update_dpid()

    def update_dpid(self):
        selected = self.ui.switch_box.currentText()
        self.ui.dpid_name.setText(self.swtich_and_dpid_dict[selected])