from search import *
from puzzle8 import *
from heapq import *

pq = []
for x in xrange(10):
    state = randomState(numMoves=x)
    node = ASNode(state)
    node.f = numWrongTiles(state)
    pq.append(node)

heapify(pq)

while len(pq) > 0:
    print heappop(pq).f

# # Test the astar search
# print "Testing astar on solution --------------------"
# s = solution()
# astar( s, numWrongTiles )

# print "Testing astar on 4-move-away -----------------"
# s = randomState(numMoves=4)
# print "original:"
# display(s)
# print ""
# astar( s, numWrongTiles )

# print "Testing astar on random state ----------------"
# r = randomState()
# astar( r, numWrongTiles )
