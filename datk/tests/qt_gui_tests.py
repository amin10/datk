from datk.core.distalgs import *
from datk.core.networks import *
from datk.core.algs import *

from helpers import Artificial_LE_Network
from mock import patch
from nose.tools import timed

Algorithm.DEFAULT_PARAMS = {"draw":False, "verbosity" : Algorithm.QUIET}

def test_network_draw_qt():
    from datk.core.simulator_qt import draw
    from PyQt4.QtGui import QApplication
    with patch.object(QApplication, 'exec_', return_value=0):
        x = Unidirectional_Ring(6)
        LCR(x)
        draw(x)

def test_network_simulate_qt():
    from datk.core.simulator_qt import simulate
    from PyQt4.QtGui import QApplication
    with patch.object(QApplication, 'exec_', return_value=0):
        x = Unidirectional_Ring(6)
        LCR(x)
        simulate(x)

@timed(18)
def test_draw_huge_random():
    from datk.core.simulator_qt import draw
    from PyQt4.QtGui import QApplication
    with patch.object(QApplication, 'exec_', return_value=0):
        x = Random_Line_Network(50, sparsity=0.2)
        draw(x)