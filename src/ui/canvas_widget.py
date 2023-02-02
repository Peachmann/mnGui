from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
from mpl_interactions import panhandler
from markers import MarkerGenerator


class CanvasWidget(QWidget):

    """
    The widget which makes up the plotting (display) part of the app.
    Relies on NetworkX for graph creation and plotting (which is build upon matplotlib).
    """

    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__()   
        self.ax = ''
        self.pan_handler = ''
        font = QFont()
        font.setPointSize(16)
        mg = MarkerGenerator()
        self.host_marker = mg.host_marker
        self.switch_marker = mg.switch_marker
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)

        self.show()

    def networkPlot(self, switches, hosts, links):
        self.figure.clf()
        self.ax = self.figure.add_subplot(111)
        self.ax.axis("off")

        G = nx.Graph()

        for switch in switches:
            G.add_node(switch['dpid'], element='Switch', name=switch['name'])

        for host in hosts:
            G.add_node(host['mac'], element='Host', name=host['name'], port=host['port']['name'])
            G.add_edge(host['mac'], host['port']['dpid'])

        for link in links:
            source = link['src']['dpid']
            destination = link['dst']['dpid']
            if int(source) < int(destination):
                G.add_edge(source, destination)

        pos = nx.spring_layout(G)

        switch_list = [x for x,y in G.nodes(data=True) if y['element'] == 'Switch']
        host_list = [x for x,y in G.nodes(data=True) if y['element'] == 'Host']

        nx.draw_networkx_edges(
            G,
            pos=pos,
            ax=self.ax,
            arrows=True,
            arrowstyle="-",
            min_source_margin=15,
            min_target_margin=15,
        )

        # Draw nodes in two batches to be able to annotate them later
        drawn_switches = nx.draw_networkx_nodes(G, pos=pos, ax=self.ax, node_size=800, linewidths=0.2, nodelist=switch_list, node_shape=self.switch_marker)
        drawn_hosts = nx.draw_networkx_nodes(G, pos=pos, ax=self.ax, node_size=800, linewidths=0.2, nodelist=host_list, node_shape=self.host_marker)
        
        # Calculate node IDs needed for the hover function
        idx_switches = {}
        idc_hosts = {}
        for idx, node in enumerate(switch_list):
            idx_switches[idx] = node
        for idx, node in enumerate(host_list):
            idc_hosts[idx] = node

        # Annotate nodes with information about them based on type
        annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(ind, idx_list):
            node_idx = ind['ind'][0]
            node = idx_list[node_idx]
            xy = pos[node]
            annot.xy = xy

            current = G.nodes[node]
            text = current['element'] + ' ' + current['name']
            if current['element'] == 'Switch':
                text = text + '\nDPID: ' + str(node).lstrip('0')
            else:
                text = text + '\nMAC: ' + node + '\nPort: ' + current['port']
            annot.set_text(text)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == self.ax:
                cont, ind = drawn_switches.contains(event)
                if cont:
                    update(ind, idx_switches)
                else:
                    cont, ind = drawn_hosts.contains(event)
                    if cont:
                        update(ind, idc_hosts)
                    if vis:
                        annot.set_visible(False)
                        self.canvas.draw_idle()

        def update(ind, idx_list):
            update_annot(ind, idx_list)
            annot.set_visible(True)
            self.canvas.draw_idle()
        
        self.pan_handler = panhandler(self.figure)
        self.canvas.mpl_connect("motion_notify_event", hover)
        self.canvas.draw_idle()