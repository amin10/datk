#WORK IN PROGRESS

import matplotlib 
from matplotlib import pyplot as plt
from colorizer import Color

class Canvas():
    def __init__(self, network):
        self.network = network
        self.n_steps = len(network._snapshots)

        self.fig, self.ax = None, None
        self.setup_fig()
        self.draw()

    def setup_fig(self):
        if self.fig is None or self.ax is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)

            self.ax.get_xaxis().set_visible(False)
            self.ax.get_yaxis().set_visible(False)

    def draw(self):
        """
        Draws the network
        """
        def setup(network):
            self.setup_fig()

        def e_draw(network, edge, color=Color.black):
            color = color.toTk()
            start, end = edge
            self.ax.plot( (start[0], end[0]), (start[1], end[1]), color)
            
        def v_draw(network, vertex, color=Color.black):
            color = color.toTk()+'o'
            x,y = vertex
            self.ax.plot( [x], [y], color)

        def show(network):
            self.fig.show()

        self.network.general_draw(v_draw, e_draw, setup=setup, show=show)


if __name__ == '__main__':
    from networks import Bidirectional_Ring
    from algs import LCR
    
    x = Bidirectional_Ring(5)
    LCR(x)

    Canvas(x)