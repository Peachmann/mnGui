"""
Class used for defining different starting topologies
"""
from mininet.topo import Topo

class SingleSwitchTopo(Topo):

    def build(self):
        self.ids = {'dpid': 1, 'host': 2, 'mac': 2}
        self.switch_info = {}
        self.s1 = self.addSwitch('s1')

        h1 = self.addHost('h1', mac="00:00:00:00:11:11")
        h2 = self.addHost('h2', mac="00:00:00:00:11:12")

        self.addLink(h1, self.s1)
        self.addLink(h2, self.s1)

        self.switch_info['1'] = {'name': 's1', 'hosts': [("h1", "00:00:00:00:00:01"), ("h2", "00:00:00:00:00:02")]}

class DualSwitchTopo(Topo):

    def build(self):
        self.switch_info = {}
        self.ids = {'dpid': 2, 'host': 3, 'mac': 3}

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1', mac="00:00:00:00:00:01")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03")

        self.addLink(s1, s2)
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)

        self.switch_info['1'] = {'name': 's1', 'hosts': [("h1", "00:00:00:00:00:01"), ("h2", "00:00:00:00:00:02")]}
        self.switch_info['2'] = {'name': 's2', 'hosts': [("h3", "00:00:00:00:00:03")]}