import sys
sys.path.append(".")
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

from topos import DualSwitchTopo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

from ui.ui_main_window import Ui_MainWindow
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

RYU_URL = 'http://0.0.0.0:8080/'


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main Window handling core app.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Testing Testing")

        self.mininet_thread = MininetThread(parent=self)
        self.mininet_thread.start()



    @pyqtSlot(str)
    def change_button_text(self, value):
        self.button.setText(value)


    def the_button_was_clicked(self):
        # values = {'name': self.button.text(), 'mac': '00:00:00:00:11:13', 'switch': 's1'}
        # self.mininet_thread.addHost(values)
        r = requests.get(RYU_URL + 'v1.0/topology/links')
        print(r.json())
        print("Clicked!")


    def closeEvent(self, event):
        try:
            print('Killing Mininet thread')
            if self.mininet_thread.isRunning():
                self.mininet_thread.net.stop()
                self.mininet_thread.quit()

        except Exception as ex_quit:
            print('Exception :', ex_quit)

class MininetThread(QThread):
    """
    The thread which is responsible for running Mininet.
    """

    addHostSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        topo = DualSwitchTopo()
        c1 = RemoteController('c1')
        self.net = Mininet(topo=topo, controller=c1)

    def run(self):
        self.net.start()
        CLI(self.net)

    def addHost(self, values):
        host_name = values.get('name')
        host_mac = values.get('mac')
        switch = self.net.get(values.get('switch'))

        new_host = self.net.addHost(name=host_name, mac=host_mac)
        new_link = self.net.addLink(new_host, switch)
        switch.attach(new_link.intf2)
        self.net.configHosts()

        return new_host

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