import sys
import requests
import logging
import re
from dialogs import AddHostDialog, AddSwitchDialog
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from json import JSONDecodeError

from topos import DualSwitchTopo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

from ui.ui_main_window import Ui_MainWindow

sys.path.append(".")

logging.basicConfig(level='INFO', format='%(levelname)s :: %(name)s :: %(message)s')

RYU_URL = 'http://0.0.0.0:8080/'
VERSION = '0.1'

LINKS_URL = RYU_URL + 'v1.0/topology/links'
SWITCHES_URL = RYU_URL + 'v1.0/topology/switches'
HOSTS_URL = RYU_URL + 'v1.0/topology/hosts'

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main Window handling core app.
    """

    logger = logging.getLogger('Main')

    add_host_signal = pyqtSignal(dict)

    ids = {'dpid': 0, 'host': 0, 'mac': 0}
    links = {}
    switches = {}
    hosts = {}

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(F"MnGUI v{VERSION}")

        # Setup Mininet Thread with required Slots and Signals
        self.mininet_thread = MininetThread(parent=self)
        self.mininet_thread.refresh_topology_signal.connect(self.refresh_topology)
        self.mininet_thread.update_ids_signal.connect(self.update_ids)
        self.add_host_signal.connect(self.mininet_thread.add_host)
        self.mininet_thread.start()

        # Setup API Slots and Signals
        self.add_host_button.clicked.connect(self.load_add_host_dialog)
        self.add_switch_button.clicked.connect(self.load_add_switch_dialog)
        self.refresh_button.clicked.connect(self.refresh_topology)

    def load_add_host_dialog(self):
        dialog = AddHostDialog(self)
        dialog.init_selections(self.switches, self.ids)

        if dialog.exec():
            new_host = {}
            new_host['name'] = dialog.ui.host_name.text()
            new_host['mac'] = dialog.ui.mac_name.text()
            new_host['switch'] = dialog.ui.switch_box.currentText()
            self.add_host_signal.emit(new_host)
            self.logger.info("Adding host.")
        else:
            self.logger.info("Canceled add host process.")

    def load_add_switch_dialog(self):
        dialog = AddSwitchDialog(self)
        dialog.populate_switch_multi_select(['s1', 's2', 's3', 's4'])

        if dialog.exec():
            self.logger.info("Adding switch.")
        else:
            self.logger.info("Canceled add switch process.")

    @pyqtSlot(dict)
    def update_ids(self, values):
        self.ids.update(values)

    @pyqtSlot()
    def refresh_topology(self):
        self.switches.clear()
        self.hosts.clear()
        self.links.clear()
        self.switches, self.hosts, self.links = self.get_full_topology()

        for switch in self.switches:
            port_name = switch['ports'][0]['name']
            switch['name'] = re.findall("([-.\w]+)-eth[\d]+", port_name)[0]

            current_dpid = int(switch['dpid'])
            if current_dpid == self.ids['dpid']:
                self.ids['dpid'] += 1

        # Add names of hosts for detailed view
        host_names = {}
        for host in self.mininet_thread.net.hosts:
            host_names[host.MAC()] = host.name

            #print(host.MAC() + ' xddd ' + host.name)
            
            current_mac = int(str(host.MAC()).rsplit(':', 1)[-1])
            if current_mac == self.ids['mac']:
                self.ids['mac'] += 1

        for host in self.hosts:
            name = host_names.get(host['mac'])
            host['name'] = name

        # Remove duplicates
        for host in self.hosts:
            if host['name'] is None:
                self.hosts.pop(self.hosts.index(host))

        self.canvas_widget.networkPlot(self.switches, self.hosts, self.links)
        self.logger.info("Topology updated.")

    @pyqtSlot()
    def get_full_topology(self):
        links = requests.get(LINKS_URL)
        switches = requests.get(SWITCHES_URL)
        hosts = requests.get(HOSTS_URL)

        try:
            links_dict = links.json()
            switches_dict = switches.json()
            hosts_dict = hosts.json()
        except JSONDecodeError:
            self.logger.error('Response could not be serialized')

        return switches_dict, hosts_dict, links_dict


    def closeEvent(self, event):
        try:
            self.logger.info('Killing Mininet thread')
            if self.mininet_thread.isRunning():
                self.mininet_thread.net.stop()
                self.mininet_thread.quit()

        except Exception as ex_quit:
            self.logger.exception(ex_quit)

class MininetThread(QThread):
    """
    The thread which is responsible for running Mininet.
    The topology modifying functions are also here.
    """

    refresh_topology_signal = pyqtSignal()
    update_ids_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.topo = DualSwitchTopo()
        c1 = RemoteController('c1')
        self.net = Mininet(topo=self.topo, controller=c1)

    def run(self):
        self.net.start()
        self.net.pingAll()
        self.update_ids_signal.emit(self.topo.ids)
        self.refresh_topology_signal.emit()

        CLI(self.net)


    @pyqtSlot(dict)
    def add_host(self, values):
        host_name = values.get('name')
        host_mac = values.get('mac')
        switch = self.net.get(values.get('switch'))

        new_host = self.net.addHost(host_name, mac=host_mac)
        new_link = self.net.addLink(new_host, switch)
        switch.attach(new_link.intf2)

        if new_host.defaultIntf():
            new_host.configDefault()

        self.msleep(500)

        self.refresh_topology_signal.emit()

        return new_host

    @pyqtSlot(dict)
    def add_switch(self, values):
        # Add new host, switch, and links to existing network
        # s1, s3 = self.net.get( 's1' ), net.addSwitch( 's3' )
        #slink = self.net.addLink( s1, s3 )

        existing_switches = self.net.get(values.get('old_switch_list'))
        new_switch = values.get('new_switch_name')

        # Configure and start up                                                                                    
        # s1.attach( slink.intf1 )
        # s3.start( self.net.controllers )

class MnGui():
    """
    Driver function.
    """

    def __init__(self, *args, **kwargs):
        super(MnGui, self).__init__(*args, **kwargs)
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        sys.exit(app.exec())

MnGui()