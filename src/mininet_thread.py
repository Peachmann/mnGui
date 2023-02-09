from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

from mininet.net import Containernet
from topos import PlainDualSwitch
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.log import info, setLogLevel


class MininetThread(QThread):
    """
    The thread which is responsible for running Mininet.
    The topology modifying functions are also here.
    """

    refresh_topology_signal = pyqtSignal()
    update_ids_signal = pyqtSignal(dict, dict)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.topo = PlainDualSwitch()
        c1 = RemoteController('c1')
        self.net = Containernet(topo=self.topo, controller=c1)

    def run(self):
        self.update_ids_signal.emit(self.topo.ids, self.topo.macs)
        self.net.start()
        self.net.pingAll()
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

    @pyqtSlot(str)
    def remove_host(self, host_name):
        host_node = self.net.get(host_name)
        self.net.delHost(host_node)
        self.msleep(500)
        self.refresh_topology_signal.emit()

    @pyqtSlot(dict)
    def add_switch(self, values):
        new_switch = self.net.addSwitch(values['name'], dpid=values['dpid'])

        for switch_name in values['link_to']:
            switch = self.net.get(switch_name)
            link = self.net.addLink(switch, new_switch)
            switch.attach(link.intf1)

        new_switch.start(self.net.controllers)

        self.msleep(500)
        self.refresh_topology_signal.emit()

    @pyqtSlot(str)
    def remove_switch(self, switch_name):
        switch_node = self.net.get(switch_name)
        self.net.delSwitch(switch_node)
        self.msleep(500)
        self.refresh_topology_signal.emit()

