from datk.core.distalgs import *
from datk.core.networks import *
from datk.core.algs import *

from helpers import Artificial_LE_Network
from mock import patch
from Tkinter import Tk
from datk.core.simulator_tk import draw, simulate, ToolTip

Algorithm.DEFAULT_PARAMS = {"draw":False, "verbosity" : Algorithm.QUIET}

def test_network_draw_tk():
    with patch.object(Tk, 'mainloop'):
        x = Unidirectional_Ring(6)
        LCR(x)
        draw(x)

def test_network_simulate_tk():
    with patch.object(Tk, 'mainloop'):
        x = Unidirectional_Ring(6)
        LCR(x)
        simulate(x)

def test_tooltip_tk():
    x = Unidirectional_Ring(6)
    LCR(x)
    x.restore_snapshot(1) #First snapshot after LCR start
    tt = ToolTip(None, x[0], 0, 0)