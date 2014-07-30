#file: hallway.py
#Use our specification to solve Littman's hallway problem

from transitionStructure import *
from specification import *
from valueIterator import *

#Run the simulation on Littman's hallway with various parameters:
def hallway(n, p):
    #n: length of hallway in the safe direction
    #p: probability of hitting wall even in safe direction
    
    #Set up the transition structure
    ts = TransitionStructure()
    ts.addAction('start','sit',{'start': 1})
    ts.addAction('start','a',{'wall': 1})
    ts.addAction('wall','a',{'goal': 1})
    ts.addAction('goal','a',{'goal': 1})
    ts.addAction('start','b',{0: 1})
    ts.addAction(0, 'a', {'wall': p, 1: 1-p})
    ts.addAction(n, 'a', {'goal': 1})
    for k in range(1, n):
        ts.addAction(k, 'a', {k+1: 1})
    
    #And the reward function
    G = lambda st: 1 if st == 'goal' else 0
    W = lambda st: 1 if st == 'wall' else 0
    S = lambda st: 1 if st == 'start' else 0
    rfs = combineReward(G, W, S)
#    worth = Lexicographic(Gt(ID(0), Number(0)), Negate(ID(1))).worth
    worth = Lexicographic(Negate(ID(2)), Negate(ID(1))).worth
    
    vi = ValueIterator(ts, rfs, worth)
    return vi

#Same hallway with movement in both directions
def twohallway(n, p):
    #n: length of hallway in the safe direction
    #p: probability of hitting wall even in safe direction
    
    #Set up the transition structure
    ts = TransitionStructure()
    ts.addAction('start','sit',{'start': 1})
    ts.addAction('start','a',{'wall': 1})
    ts.addAction('wall', 'z',{'start': 1})
    ts.addAction('wall','a',{'goal': 1})
    ts.addAction('goal','z',{'wall': 1})
    ts.addAction('goal','a',{'goal': 1})
    ts.addAction('start','b',{0: 1})
    ts.addAction(0, 'y', {'start': 1})
    ts.addAction(0, 'a', {'wall': p, 1: 1-p})
    ts.addAction(1, 'z', {0: 1})
    ts.addAction(n, 'a', {'goal': 1})
    ts.addAction('goal', 'y', {n: 1})
    for k in range(1, n):
        ts.addAction(k, 'a', {k+1: 1})
        ts.addAction(k+1, 'z', {k: 1})
    
    #And the reward function
    G = lambda st: 1 if st == 'goal' else 0
    W = lambda st: 1 if st == 'wall' else 0
    S = lambda st: 1 if st == 'start' else 0
    rfs = combineReward(G, W, S)
#    worth = Lexicographic(Gt(ID(0), Number(0)), Negate(ID(1))).worth
    worth = Lexicographic(Negate(ID(2)), Negate(ID(1)), ID(0)).worth
    
    vi = ValueIterator(ts, rfs, worth)
    return vi

def test():
    for n in range(1,11):
        for p in [.1*x for x in range(11)]:
            vi = hallway(n, p)
            print "%5d %5.2f %s" % (n, p, vi.policy('start'))
    
if __name__ == '__main__':
    vi = twohallway(2, .3)
    vi.displayPolicy()
