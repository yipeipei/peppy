import os

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

__author__ = 'Peipei YI'


def draw_graph(fname, skip_header=0):
    data = np.genfromtxt(fname, dtype=np.uint32, skip_header=skip_header)
    g = nx.DiGraph(data.tolist())
    # nx.shell_layout(g)
    nx.draw(g)
    plt.title(os.path.basename(fname))
    plt.show()


if __name__ == '__main__':
    path = raw_input("path or file name:").strip('"')
    draw_graph(path)