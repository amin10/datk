from distalgs import *
from networks import *
from algs import *
from tester import *
begin_testing()

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
    LCR(r, test_params)
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
    g = Random_Network(16)
    FloodMax(g, params = test_params)
    testLeaderElection(g)

@test
def SYNCH_BFS():
    x = Random_Network(10)
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
    x = Random_Network(10)

    FloodMax(x, test_params)
    testLeaderElection(x)

    SynchBFS(x, test_params)
    testBFS(x)

    SynchConvergeHeight(x, test_params)

@test
def SYNCH_BROADCAST_HEIGHT():
    x = Random_Network(10)

    FloodMax(x, test_params)
    testLeaderElection(x)

    SynchBFSAck(x, test_params)
    testBFSWithChildren(x)

    SynchConvergeHeight(x, test_params)

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
    x[2].send_msg(a3)
    x[0].send_msg(b1)
    x[2].send_msg(b2)

    assert x[1].get_msgs(B) == [b1,b2]
    assert x[1].get_msgs(A, x[0]) == [a1, a2]
    assert x[1].get_msgs(A, x[0]) == []
    assert x[1].get_msgs(A) == [a3]
    assert x[1].get_msgs(A) == []

@test
def SYNCH_DO_NOTHING():
    x = Random_Network(5)
    state = x.state()
    Do_Nothing(x)
    assert state == x.state()

@test
def COMPOSE_SYNCH_LCR_AND_DO_NOTHING():
    A = Compose(LCR(), Do_Nothing())
    x = Unidirectional_Ring(5)
    A(x)
    testLeaderElection(x)

@test(timeout=2)
def COMPOSE_SYNCH_LCR_AND_LCR():
    A = Compose(LCR(name="B"), LCR(name="C"))
    x = Unidirectional_Ring(5)
    A(x, params=test_params)
    testLeaderElection(x)

summarize()