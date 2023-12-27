from apxo.tests.infrastructure import *
startfile(__file__, "propeller power")

# Propeller Power

starttestsetup()
A1 = aircraft("A1", "AF", "AD-4", "2015", "N", 10, 2.0, "CL")
A2 = aircraft("A2", "AF", "AD-4", "2215", "N", 10, 2.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "M", "")
asserterror("aircraft does not have an M power setting.")
A1.move("LVL",  "AB", "")
asserterror("aircraft does not have an AB power setting.")
A1.move("LVL",  2, "")
asserterror("requested power of 2 APs exceeds aircraft capability.")
A1.move("LVL",  "FT", "H,H")
A1._assert("A1-2013       N    10",  2.0)
A2.move("LVL",  "HT", "H,H")
A2._assert("A1-2213       N    10",  2.0)
endturn()

startturn()
A1.move("LVL",  "FT", "H,H")
A1._assert("A1-2011       N    10",  2.5)
A2.move("LVL",  "HT", "H,H")
A2._assert("A1-2211       N    10",  2.0)
endturn()

startturn()
A1.move("LVL",  1.5, "H,H")
A1._assert("A1-2009       N    10",  3.0)
A2.move("LVL",  0.5, "H,H")
A2._assert("A1-2209       N    10",  2.0)
endturn()

startturn()
A1.move("LVL",  1.0, "H,H,H")
A1._assert("A1-2006       N    10",  3.0)
A2.move("LVL",  0.5, "H,H")
A2._assert("A1-2207       N    10",  2.5)
endturn()

# Power Fade

starttestsetup()
A1 = aircraft("A1", "AF", "Sea Fury FB.11", "2015", "N", 10, 4.5, "CL")
A2 = aircraft("A2", "AF", "Sea Fury FB.11", "2215", "N", 10, 3.5, "CL")
A3 = aircraft("A3", "AF", "Sea Fury FB.11", "2415", "N", 10, 3.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  2.0, "H,H,H,H")
asserterror("requested power of 2.0 APs exceeds aircraft capability.")
startturn()
A1.move("LVL",  1.5, "H,H,H,H")
asserterror("requested power of 1.5 APs exceeds aircraft capability.")
startturn()
A1.move("LVL",  1.0, "H,H,H,H")
A1._assert("A1-2011       N    10",  4.5)
startturn()
A2.move("LVL",  2.0, "H,H,H,H")
asserterror("requested power of 2.0 APs exceeds aircraft capability.")
startturn()
A2.move("LVL",  1.5, "H,H,H"  )
A2._assert("A1-2212       N    10",  3.5)
startturn()
A3.move("LVL",  2.0, "H,H,H"  )
A3._assert("A1-2412       N    10",  3.5)
startturn()
A1.move("LVL",  "FT", "H,H,H,H")
A1._assert("A1-2011       N    10",  4.5)
A2.move("LVL",  "FT", "H,H,H"  )
A2._assert("A1-2212       N    10",  3.5)
A3.move("LVL",  "FT", "H,H,H"  )
A3._assert("A1-2412       N    10",  3.5)
endturn()

startturn()
A1.move("LVL",  "FT", "H,H,H,H,H")
A1._assert("A1-2006       N    10",  4.5)
A2.move("LVL",  "FT", "H,H,H,H"  )
A2._assert("A1-2208       N    10",  4.0)
A3.move("LVL",  "FT", "H,H,H"    )
A3._assert("A1-2409       N    10",  3.5)
endturn()

startturn()
A1.move("LVL",  "FT", "H,H,H,H"  )
A1._assert("A1-2002       N    10",  4.5)
A2.move("LVL",  "FT", "H,H,H,H"  )
A2._assert("A1-2204       N    10",  4.5)
A3.move("LVL",  "FT", "H,H,H,H"  )
A3._assert("A1-2405       N    10",  4.0)
endturn()

endfile(__file__)