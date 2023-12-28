from apxo.tests.infrastructure import *
startfile(__file__, "banking")


# Turns and banking with normal RR aircraft

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C" , "A1-2015", "N"  , 10, 4.0, "CL")
endtestsetup()
startturn()
A1.move("LVL",  "M", "H/WL,EZL/H,H,H")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/WL,EZR/H,H,H")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BL,EZR/H,H,H")
asserterror("attempt to declare a turn to R while banked to L.")
startturn()
A1.move("LVL",  "M", "H/BR,EZL/H,H,H")
asserterror("attempt to declare a turn to L while banked to R.")
startturn()
A1.move("LVL",  "M", "H/BL,H/BR,H,H")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BR,H/BL,H,H")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BR,H/WL,H/BL,H/WL")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BR,EZR/H,H,HR")
A1._assert("A1-2011       NNE  10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BL,EZL/H,H,HL")
A1._assert("A1-2011       NNW  10",  4.0)
endturn()

# Turns and banking with LRR aircraft

starttestsetup()
A1 = aircraft("A1", "AF", "Meteor F.8" , "A1-2015", "N"  , 10, 4.0, "CL")
endtestsetup()
startturn()
A1.move("LVL",  "M", "H/WL,EZL/H,H,H")
asserterror("attempt to declare a turn to L while not banked to L in a LRR aircraft.")
startturn()
A1.move("LVL",  "M", "H/WL,EZR/H,H,H")
asserterror("attempt to declare a turn to R while not banked to R in a LRR aircraft.")
startturn()
A1.move("LVL",  "M", "H/BL,EZR/H,H,H")
asserterror("attempt to declare a turn to R while not banked to R in a LRR aircraft.")
startturn()
A1.move("LVL",  "M", "H/BR,EZL/H,H,H")
asserterror("attempt to declare a turn to L while not banked to L in a LRR aircraft.")
startturn()
A1.move("LVL",  "M", "H/BL,H/BR,H,H")
asserterror("attempt to bank to R while banked to L in a LRR aircraft.")
startturn()
A1.move("LVL",  "M", "H/BR,H/BL,H,H")
asserterror("attempt to bank to L while banked to R in a LRR aircraft.")
startturn()
A1.move("LVL",  "M", "H/BR,H/WL,H/BL,H/WL")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BR,EZR/H,H,HR")
A1._assert("A1-2011       NNE  10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BL,EZL/H,H,HL")
A1._assert("A1-2011       NNW  10",  4.0)
endturn()

# Turns and banking with HRR aircraft

starttestsetup()
A1 = aircraft("A1", "AF", "F-5A" , "A1-2015", "N"  , 10, 4.0, "CL")
endtestsetup()
startturn()
A1.move("LVL",  "M", "H/WL,EZL/H,H,H")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/WL,EZR/H,H,H")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BL,EZR/H,H,H")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BR,EZL/H,H,H")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BL,H/BR,H,H" )
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BR,H/BL,H,H" )
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BR,H/WL,H/BL,H/WL")
A1._assert("A1-2011       N    10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BR,EZR/H,H,HR")
A1._assert("A1-2011       NNE  10",  4.0)
startturn()
A1.move("LVL",  "M", "H/BL,EZL/H,H,HL")
A1._assert("A1-2011       NNW  10",  4.0)
endturn()

# Turns and banking with HRRCL aircraft

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "Yak-9D" , "A1-2010", "N"  , 10, 3.5, "CL")
A2 = aircraft("A2", "AF", "Yak-9D" , "A1-2210", "N"  , 10, 3.5, "1/2")
A3 = aircraft("A3", "AF", "Yak-9D" , "A1-2410", "N"  , 10, 3.0, "DT")
endtestsetup()

startturn()
A1.move("LVL",  "HT", "BTL/H,BTR/H,H")
A1._assert("A1-2007       N    10",  3.5)
startturn()
A2.move("LVL",  "HT", "BTL/H,BTR/H,H")
asserterror("attempt to declare a turn to R while banked to L.")
startturn()
A2.move("LVL",  "HT", "BTL/H,WL/H,BTR/H")
A2._assert("A1-2207       N    10",  3.5)
startturn()
A3.move("LVL",  "HT", "HTL/H,HTR/H,H")
asserterror("attempt to declare a turn to R while banked to L.")
startturn()
A3.move("LVL",  "HT", "HTL/H,WL/H,HTR/H")
A3._assert("A1-2407       N    10",  3.0)
endturn()

endfile(__file__)