"""
Algorithm Test Suite

Tests algorithms defined in algs.py
"""

try:
    from datk.core.distalgs import *
    from datk.core.networks import *
    from datk.core.algs import *
    from datk.core.tester import *
except ImportError:
    raise ImportError(
""" Imports failed\n
To run tests, execute the following commands:
$ cd ../..
$ python -m datk.tests.tests """)
from helpers import *

def configure_ipython():
  """
  Convenient helper function to determine if environment is ipython.
  Note that drawing is only safe in ipython qtconsole with matplotlib inline
  If environment is IPython, returns True and configures IPython.
  Else returns False.
  """
  try:
    __IPYTHON__
    ip = get_ipython()
    ip.magic("%matplotlib inline") 
  except NameError:
    return False
  else:
    return True

in_ipython = configure_ipython()

test_params = {"draw":False, "silent" : True}

@test
def LCR_UNI_RING():
    r = Unidirectional_Ring(6)
    LCR(r, params=test_params)
    testLeaderElection(r)

@test
def LCR_BI_RING():
    r = Bidirectional_Ring(6)
    LCR(r, params = test_params)
    testLeaderElection(r)

@test
def ASYNC_LCR_UNI_RING():
    r = Unidirectional_Ring(6)
    AsyncLCR(r, params = test_params)
    testLeaderElection(r)

@test
def ASYNC_LCR_BI_RING():
    r = Bidirectional_Ring(6)
    AsyncLCR(r, params = test_params)
    testLeaderElection(r)

@test
def FLOODMAX_UNI_RING():
    r = Unidirectional_Ring(4)
    FloodMax(r, params = test_params)
    testLeaderElection(r)

@test
def FLOODMAX_BI_RING():
    r = Bidirectional_Ring(4)
    FloodMax(r, params = test_params)
    testLeaderElection(r)

@test
def FLOODMAX_BI_LINE():
    l = Bidirectional_Line(4)
    FloodMax(l, params = test_params)
    testLeaderElection(l)

@test
def FLOODMAX_COMPLETE_GRAPH():
    g = Complete_Graph(10)
    FloodMax(g, params = test_params)
    testLeaderElection(g)

@test
def FLOODMAX_RANDOM_GRAPH():
    g = Random_Line_Network(16)
    FloodMax(g, params = test_params)
    testLeaderElection(g)

@test
def SYNCH_BFS():
    x = Random_Line_Network(10)
    FloodMax(x, test_params)
    testLeaderElection(x)

    SynchBFS(x, test_params)
    testBFS(x)

@test
def SYNCH_BFS_ACK():
    x = Bidirectional_Line(6, lambda t:t)

    FloodMax(x, test_params)
    testLeaderElection(x)

    SynchBFSAck(x, test_params)
    testBFSWithChildren(x)

@test
def SYNCH_CONVERGE_HEIGHT():
    x = Random_Line_Network(10)

    FloodMax(x, test_params)
    testLeaderElection(x)

    SynchBFS(x, test_params)
    testBFS(x)

    SynchConvergeHeight(x, test_params)

@test
def SYNCH_BROADCAST_HEIGHT():
    x = Random_Line_Network(10)

    FloodMax(x, test_params)
    testLeaderElection(x)

    SynchBFSAck(x, test_params)
    testBFSWithChildren(x)

    SynchConvergeHeight(x, test_params)

    SynchBroadcast(x, {"attr":"height", "draw":in_ipython, "silent" : True})
    testBroadcast(x, 'height')

@test
def ASYNCH_BROADCAST_HEIGHT():
    x = Random_Line_Network(10)

    FloodMax(x, test_params)
    testLeaderElection(x)

    SynchBFSAck(x, test_params)
    testBFSWithChildren(x)

    AsynchConvergeHeight(x, test_params)

    SynchBroadcast(x, {"attr":"height", "draw":in_ipython, "silent" : True})
    testBroadcast(x, 'height')

@test
def send_receive_msgs():
    A = LCR()
    a1 = Message(A)
    a2 = Message(A)
    a3 = Message(A)

    B = LCR()
    b1 = Message(B)
    b2 = Message(B)

    x = Bidirectional_Ring(4, lambda p:p)
    assert x[0].get_msgs(A) == []
    x[0].send_msg(a1)
    x[0].send_msg(a2)
    assert a1.author == x[0] and a2.author == x[0]
    x[2].send_msg(a3)
    assert a3.author == x[2]
    x[0].send_msg(b1)
    assert b1.author == x[0]
    x[2].send_msg(b2)
    assert b2.author == x[2]

    assert x[1].get_msgs(B) == [b1,b2]
    assert x[1].get_msgs(A, x[0]) == [a1, a2]
    assert x[1].get_msgs(A, x[0]) == []
    assert x[1].get_msgs(A) == [a3]
    assert x[1].get_msgs(A) == []

@test
def SYNCH_DO_NOTHING():
    x = Random_Line_Network(5)
    state = x.state()
    assert Do_Nothing(x, params=test_params).message_count == 0
    assert state == x.state()

@test
def COMPOSE_SYNCH_LCR_AND_DO_NOTHING():
    x = Unidirectional_Ring(5)
    x1 = x.clone()

    A = LCR(params = test_params)
    A(x)
    testLeaderElection(x)

    C = Compose(LCR(params = test_params), Do_Nothing())
    C(x1, params=test_params)
    testLeaderElection(x1)

    assert C.message_count == A.message_count, "Wrong message count"

@test
def COMPOSE_SYNCH_LCR():
    x = Unidirectional_Ring(10)
    x1 = x.clone()
    x2 = x.clone()

    A = LCR()
    A(x, params = test_params)
    testLeaderElection(x)

    B = Compose(LCR(name="B1", params = test_params), LCR(name="B2", params = test_params))
    B(x1)
    testLeaderElection(x1)

    C = Compose(Compose(LCR(params = test_params), LCR(params = test_params)), LCR(params = test_params))
    C(x2)
    testLeaderElection(x2)

    assert B.message_count == 2*A.message_count, "Compose LCR LCR wrong message count"
    assert C.message_count == 3*A.message_count, "Compose LCR LCR LCR wrong message count"

@test
def CHAIN_BROADCAST_HEIGHT():
    fm = FloodMax()
    bfs = SynchBFSAck()
    converge = SynchConvergeHeight()
    broadcast = SynchBroadcast(params ={"attr":"height","draw":in_ipython, "silent":True})

    A = Chain(Chain(fm, bfs), Chain(converge, broadcast))
    x = Random_Line_Network(10)
    A(x)
    testLeaderElection(x)
    testBFSWithChildren(x)
    testBroadcast(x, 'height')

@test
def SYNCH_LUBY_MIS_BI_RING():
    x = Bidirectional_Ring(10, lambda t:t)
    SynchLubyMIS(x, params=test_params)
    testLubyMIS(x)

@test
def SYNCH_LUBY_MIS():
    x = Random_Line_Network(10)
    SynchLubyMIS(x)
    testLubyMIS(x)

summarize()
