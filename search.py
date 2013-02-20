########################################################################
# Daniel Friedman, Donal Sheets, Luke Lovett                           #
# HW1                                                                  #
# We affirm that we have adhered to the Honor Code in this assignment. #
########################################################################
from puzzle8 import *

# 
# Heuristic helper functions
# 
def numWrongTiles( state ):
    '''Returns the number of misplaced tiles for the indicated state'''
    sol = solution()
    count = 0
    
    for square in xrange(9):
        if getTile(state, square) != getTile(sol, square):
            count += 1

    return count

def manhattanDistance( state ):
    '''Returns the manhattan distance for each position in <state>, respectively'''
    distances = []
    soln = solution()

    state_list = [getTile(state,i) for i in xrange(9)]
    soln_list = [getTile(soln,i) for i in xrange(9)]

    for i in xrange(9):
        our_position = xylocation(i)
        soln_position = xylocation(soln_list.index(state_list[i]))
        distances.append( sum([abs(x-y) for x,y in zip(our_position,soln_position)]) )

    return distances

#
# Search algorithms
#
def state_neighbors( state ):
    '''Returns the neighbors of the configuration given in <state>.'''
    blank = blankSquare( state )
    blank_neighbors = neighbors( blank )

    return [moveBlank(state,n) for n in blank_neighbors]

def is_goal(s):
    return solution() == s

def itdeep_helper( state, maxdepth ):
    if maxdepth is 0:
        return
    itdeep_helper( n, maxdepth-1)

def itdeep( state ):
    '''Runs iterative deepening starting from <state>. Returns a list
    of moves for the blank tile to solve the 8-puzzle.'''

    depth = 1
    moves = []
    fringe = [state]
    
    while len(fringe) > 0 and depth > 0:
        cur_state = fringe.pop()
        moves.append(blankSquare(cur_state))

        # Test if current state is our goal
        if is_goal( cur_state ):
            return moves

        neighbors = state_neighbors(cur_state)
        # Test neighbors to see if any are goal cur_states
        for n in neighbors:
            if is_goal(n):
                return moves + blankSquare(n)
            fringe.append(n)
        
