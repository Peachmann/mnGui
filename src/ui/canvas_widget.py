from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
import numpy as np
import PIL
from mpl_interactions import panhandler



class CanvasWidget(QWidget):

    def __init__(self, parent=None):

        super(CanvasWidget, self).__init__()   

        icons = {
            "switch": "resources/switch.png",
            "host": "resources/host.png",
        }
        self.images = {k: PIL.Image.open(fname) for k, fname in icons.items()}
        self.ax = ''
        self.pan_handler = ''
        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)
        self.canvas.mpl_connect('button_press_event', self.drag_event)

        #self.networkPlot()
        self.plot1()
        self.show()

    def networkPlot(self, switches, hosts, links):
        self.figure.clf()
        self.ax = self.figure.add_subplot(111)
        self.ax.axis("off")

        G = nx.Graph()

        for switch in switches:
            G.add_node(switch['dpid'], element='Switch', image=self.images["switch"], name=switch['name'])

        for host in hosts:
            G.add_node(host['mac'], element='Host', image=self.images["host"], name=host['name'], port=host['port']['name'])
            G.add_edge(host['mac'], host['port']['dpid'])

        # Switch links
        for link in links:
            source = link['src']['dpid']
            destination = link['dst']['dpid']
            if int(source) < int(destination):
                G.add_edge(source, destination)

        pos = nx.spring_layout(G, seed=123456789)

        nx.draw_networkx_edges(
            G,
            pos=pos,
            ax=self.ax,
            arrows=True,
            arrowstyle="-",
            min_source_margin=15,
            min_target_margin=15,
        )

        tr_figure = self.ax.transData.transform
        tr_axes = self.figure.transFigure.inverted().transform

        # Select the size of the image (relative to the X axis)
        icon_size = (self.ax.get_xlim()[1] - self.ax.get_xlim()[0]) * 0.025
        icon_center = icon_size / 2.0
        
        icons_axes = []

        # Add the respective image to each node
        for node in G.nodes:
            xf, yf = tr_figure(pos[node])
            xa, ya = tr_axes((xf, yf))
            # get overlapped axes and plot icon
            a = self.figure.add_axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
            a.imshow(G.nodes[node]['image'])
            a.axis("off")
            icons_axes.append(a)

            current = G.nodes[node]
            text = current['element'] + ' ' + current['name']
            if current['element'] == 'Switch':
                text = text + '\nDPID: ' + str(node).lstrip('0')
            else:
                text = text + '\nMAC: ' + node + '\nPort: ' + current['port']

            a.annot = a.annotate(text, xy=(0,0),
                    bbox=dict(boxstyle="round", fc="w"))
            a.annot.set_visible(False)

        def enter_axes(event):
            if event.inaxes in icons_axes:
                event.inaxes.annot.set_visible(True)
                self.canvas.draw_idle()

        def leave_axes(event):
            if event.inaxes in icons_axes:
                event.inaxes.annot.set_visible(False)
                self.canvas.draw_idle()
        
        self.canvas.mpl_connect('axes_enter_event', enter_axes)
        self.canvas.mpl_connect('axes_leave_event', leave_axes)
        self.pan_handler = panhandler(self.figure)
        self.canvas.draw_idle()

    def drag_event(self, event):
        return xd


    def plot1(self):
        self.figure.clf()
        B = nx.Graph()
        B.add_nodes_from([1, 2, 3, 4], bipartite=0)
        B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        B.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])

        X = set(n for n, d in B.nodes(data=True) if d['bipartite'] == 0)
        Y = set(B) - X

        X = sorted(X, reverse=True)
        Y = sorted(Y, reverse=True)

        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
        nx.draw(B, pos=pos, with_labels=True)
        self.canvas.draw_idle()