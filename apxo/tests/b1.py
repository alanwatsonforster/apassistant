from apxo.tests.infrastructure import *

startfile(__file__, "order of actions")

# Check basic movement.

# H movements.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "N", 10, 2.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "WL/H")
asserterror("unexpected WL action in move prolog.")

startgameturn()
A1.move("LVL", "M", "H/TTR")
asserterror("unexpected TTR action in move epilog.")
