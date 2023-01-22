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



class CanvasWidget(QWidget):

    def __init__(self, parent=None):

        super(CanvasWidget, self).__init__()   

        icons = {
            "switch": "resources/switch.png",
            "host": "resources/host.png",
        }
        self.images = {k: PIL.Image.open(fname) for k, fname in icons.items()}
        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)
        self.ax.axis("off")

        #self.networkPlot()
        self.plot1()
        self.show()

    def networkPlot(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.axis("off")

        G = nx.Graph()

        G.add_node("switch_1", image=self.images["switch"])
        for j in range(1, 4):
            G.add_node("host_1_" + str(j), image=self.images["host"])
        
        for v in range(1, 4):
            G.add_edge("switch_1", "host_1_" + str(v))

        pos = nx.spring_layout(G)

        nx.draw_networkx_edges(
            G,
            pos=pos,
            ax=ax,
            arrows=True,
            arrowstyle="-",
            min_source_margin=15,
            min_target_margin=15,
        )

        tr_figure = ax.transData.transform
        tr_axes = self.figure.transFigure.inverted().transform

        # Select the size of the image (relative to the X axis)
        icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.025
        icon_center = icon_size / 2.0

        # Add the respective image to each node
        for n in G.nodes:
            xf, yf = tr_figure(pos[n])
            xa, ya = tr_axes((xf, yf))
            # get overlapped axes and plot icon
            a = self.figure.add_axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
            a.imshow(G.nodes[n]["image"])
            a.axis("off")

        self.canvas.draw_idle()



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