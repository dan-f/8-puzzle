8-puzzle
========

Solving the 8-puzzle with advanced search algorithms.

Authors: Dan Friedman, Luke Lovett, Donal Sheets
We have all adhered to the Honor Code on this assignment.

### Notes

Our 'astar' search function takes an optional keyword argument 'use_explored',
which when set to True will keep track of explored nodes. We highly recommend
setting this argument, as it will **dramatically** improve speed!!!

#### A typical call to our astar search:
`
astar( randomState(), numWrongTiles )
`
This could take a long time. Grab a beer!

#### A better call to our astar search:
`
astar( randomState(), numWrongTiles, use_explored=True )
`
Ahhh, that's much better (order of minutes)!!

#### Testing

All of our tests are in test.py. This script will take a long time to run,
because neither search attempts to keep track of visited states in our
tests. You can choose to ignore this file if you wish.
