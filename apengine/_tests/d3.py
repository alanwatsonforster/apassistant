from apengine._tests.infrastructure import *
startfile(__file__, "LBR/HBR aircraft")

# Sustained turns with LBR aircraft.

starttestsetup()
A1 = aircraft("A1", "Sea Fury FB.11", "2010", "N", 10, 4.5, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "FT", "BTR/H/RR,BTR/H/RR,BTR/H/RR,BTR/H/RR")
A1._assert("2210       WSW  10",  4.0)
endturn()

startturn()
A1.move("LVL",  "FT", "BTR/H/RR,BTR/H/RR,BTR/H/RR,BTR/H/RR")
A1._assert("2108       ESE  10",  3.5)
endturn()

startturn()
A1.move("LVL",  "FT", "BTR/H/RRR,BTR/H/RRR,BTR/H/RRR,HTR/H/RR")
A1._assert("2108       E    10",  2.5)
endturn()

startturn()
A1.move("LVL",  "FT", "HTR/H/RRR,HTR/H/RRR")
A1._assert("2210       W    10",  2.5)
endturn()

startturn()
A1.move("LVL",  "FT", "HTR/H/RRR,HTR/H/RRR,HTR/H/RRR")
A1._assert("2209       S    10",  2.5)
endturn()

# Sustained turns with HBR aircraft

starttestsetup()
A1 = aircraft("A1", "F7U-3", "2010", "N", 10, 6.5, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "AB", "ETR/H/R,ETR/H/R,ETR/H/R,ETR/H/R,ETR/H/R,ETR/H/R")
A1._assert("2410       S    10",  4.0)
endturn()

startturn()
A1.move("LVL",  "AB", "BTR/H/RR,BTR/H/RR,BTR/H/RR,BTR/H/RR")
A1._assert("2210       ENE  10",  1.5)
endturn()

endfile(__file__)