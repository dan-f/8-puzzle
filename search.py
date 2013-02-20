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

def to_move_list( moves ):
    '''Turns a list sequential positions of the blank tile in <moves>
    and puts them into a list of moves in the format specified in the
    lab writeup
    '''
    return [[i,j] for i,j in zip(moves[:-1],moves[1:])]

def is_goal(s):
    return solution() == s

def itdeep_helper( state, maxdepth ):
    # Base case
    if maxdepth == 0:
        return []

    moves = [blankSquare( state )]

    # We found it
    if is_goal( state ):
        return moves

    # Loop through neighbors
    ns = state_neighbors( state )
    for n in ns:
        deeper_moves = itdeep_helper(n, maxdepth-1)
        if len(deeper_moves) > 0:
            moves.extend( deeper_moves )
            return moves
    return []
        
def itdeep( state ):
    '''Runs iterative deepening starting from <state>. Returns a list
    of moves for the blank tile to solve the 8-puzzle.'''

    depth = 1

    # The trivial case
    if is_goal( state ):
        return [blankSquare(state)]

    # Do iterative deepening
    solution = itdeep_helper( state, depth )
    while len(solution) == 0:
        solution = itdeep_helper( state, depth )
        depth += 1

    return to_move_list( solution )
