from search import *
from puzzle8 import *

# Make some puzzles to solve
trivial = solution()
easy = 219235348
medium = 247856372
hard = 40013692

tests = (trivial,easy,medium,hard)

print "Testing iterative deepening"
print "---------------------------"

for test in tests:
    print "initial state:"
    display(test)
    print itdeep(test)
    print 20*'-'

print "Testing A* search"
print "-----------------"

strategies = (numWrongTiles,manhattanDistance)
for strategy in strategies:
    title = "Using heuristic: %s"%strategy.__name__
    print title
    print len(title)*'-'
    for test in tests:
        print "initial state:"
        display(test)
        print astar(test, strategy)
        print 20*'-'
