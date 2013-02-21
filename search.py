########################################################################
# Daniel Friedman, Donal Sheets, Luke Lovett                           #
# HW1                                                                  #
# We affirm that we have adhered to the Honor Code in this assignment. #
########################################################################
from puzzle8 import *
from heapq import *

# 
# Heuristic functions
# 
def numWrongTiles( state ):
    '''Returns the number of misplaced tiles for the indicated <state>.'''
    sol = solution()
    count = 0
    
    for square in xrange(9):
        if getTile(state, square) != getTile(sol, square):
            count += 1

    return count

def manhattanDistance( state ):
    '''Returns the sum of the manhattan distances for each position in <state>.'''
    distances = []
    soln = solution()

    state_list = [getTile(state,i) for i in xrange(9)]
    soln_list = [getTile(soln,i) for i in xrange(9)]

    for i in xrange(9):
        our_position = xylocation(i)
        soln_position = xylocation(soln_list.index(state_list[i]))
        distances.append( abs(our_position[0]-soln_position[0]) +
                          abs(our_position[1]-soln_position[1]) )

    return sum(distances)

#
# Search algorithm helper functions
#
def state_neighbors( state ):
    '''Returns the neighbors of the configuration given in <state>.'''
    blank = blankSquare( state )
    blank_neighbors = neighbors( blank )
    return [moveBlank(state,n) for n in blank_neighbors]

def to_move_list( moves ):
    '''Turns a list sequential positions of the blank tile in <moves>
    and puts them into a list of moves in the format specified in the
    lab writeup.
    '''
    return [[i,j] for i,j in zip(moves[:-1],moves[1:])]

def is_goal(s):
    '''A simple way to test if state <s> is the solution'''
    return solution() == s

# 
# Iterative deepening
# 
def _itdeep_helper( state, maxdepth ):
    '''Recursive DFS algorithm'''
    # Base case
    if maxdepth == 0:
        return []

    # We found it
    if is_goal( state ):
        return [blankSquare( state )]

    # Loop through neighbors in reverse order, per the lab
    # instructions (we're recursive, not explicit stack-based)
    for n in reversed( state_neighbors(state) ):
        deeper_moves = _itdeep_helper(n, maxdepth-1)
        if len(deeper_moves) > 0:
            return [blankSquare( state )] + deeper_moves
    return []
        
def itdeep( state ):
    '''Runs iterative deepening starting from <state>. Returns a list
    of moves for the blank tile to solve the 8-puzzle.
    '''

    depth = 1

    # The trivial case
    if is_goal( state ):
        place = blankSquare(state)
        return [[place,place]]

    # Do iterative deepening
    solution = _itdeep_helper( state, depth )
    while len(solution) == 0:
        solution = _itdeep_helper( state, depth )
        depth += 1

    return to_move_list( solution )

#
# A* search
# 
class ASNode(object):
    """Represents a node in the A* search algorithm."""

    def __init__(self, state):
        self.state = state
        self.prev = None
        self.f = float('inf')
        self.g = 0
        self.h = 0

    def __cmp__(self, other):
        '''This is useful for sorting within a heap.'''
        return 1 if self.f > other.f else 0 if self.f == other.f else -1

def astar( state, heuristic, use_explored=False ):
    '''Runs an A* search for a solution to the 8-puzzle, starting from
    the configuration given by <state>, and calculating heuristic
    values using <heuristic>. Optionally, make things A LOT FASTER by
    keeping track of explored nodes.
    '''
    def contains_node( l, node ):
        '''Check if the state in <node> is somewhere in a node contained in <l>'''
        return node.state in [n.state for n in l]

    def reconstruct_moves( finish ):
        '''Returns the list of moves the blank tile made to result in
        the <finish> state.
        '''
        moves = [blankSquare(finish.state)]
        cur_node = finish.prev
        while cur_node is not None:
            moves.append(blankSquare(cur_node.state))
            cur_node = cur_node.prev
        return to_move_list([x for x in reversed(moves)])
        
    # check goal state
    if is_goal(state):
        place = blankSquare(state)
        return [[place,place]]

    cur_node = ASNode(state)
    cur_node.h = heuristic(state)
    cur_node.f = 0

    pq = []
    heappush(pq, cur_node)

    explored = []
    state_map = { state:cur_node }

    # While our priority queue is non-empty
    while len(pq) > 0:
        v = heappop(pq)

        if is_goal(v.state):
            return reconstruct_moves( v )

        if use_explored:
            explored.append(v)

        # Iterate through neighbors backwards
        for neighbor in reversed(state_neighbors(v.state)):
            # Get corresponding ASNode for neighbor or create it
            if neighbor in state_map:
                nn = neighbor
                neighbor = state_map.get(neighbor)
            else:
                node = ASNode(neighbor)
                node.h = heuristic(neighbor)
                state_map[neighbor] = node
                neighbor = node

            if use_explored and neighbor in explored:
                continue

            # Update the neighbor's value for f, possibly adding it to the P.Q.
            if v.g + neighbor.h < neighbor.f or not contains_node(pq, neighbor):
                neighbor.prev = v
                neighbor.g = neighbor.prev.g + 1
                neighbor.f = v.g + 1 + neighbor.h

                if not contains_node(pq, neighbor):
                    heappush(pq, neighbor)
                else:
                    heapify(pq)
