from apxo.tests.infrastructure import *

startfile(__file__, "speed")

# Speed limits

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "N", 20, 5.0, "CL")
endtestsetup()
startgameturn()
A1.move("SD", "M", "H,H,D2,D2,D2")
A1._assert("A1-1113       N    14", 6.0)
endgameturn()
startgameturn()
A1.move("SD", "M", "H,H,D2,D2,D2,D2")
A1._assert("A1-1111       N     6", 6.5)
endgameturn()
startgameturn()
A1.move("SD", "M", "H,H,H,H,H,D2")
A1._assert("A1-1106       N     4", 6.5)
startgameturn()
A1.move("SD", "M", "H,H,H,H,H,D")
A1._assert("A1-1106       N     5", 5.5)
endgameturn()

# Acceleration and deceleration

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "N", 10, 2.5, "CL")
A2 = aircraft("A2", "AF", "F-80C", "A1-1315", "N", 10, 3.0, "CL")
A3 = aircraft("A3", "AF", "F-80C", "A1-1515", "N", 10, 3.5, "CL")
A4 = aircraft("A4", "AF", "F-80C", "A1-1715", "N", 10, 4.0, "CL")
endtestsetup()

A1._assert("A1-1115       N    10", 2.5)
A2._assert("A1-1315       N    10", 3.0)
A3._assert("A1-1515       N    10", 3.5)
A4._assert("A1-1715       N    10", 4.0)

startgameturn()
A1.move("LVL", "M", "H,H")
A1._assert("A1-1113       N    10", 2.5)
A2.move("LVL", "M", "H,H,H")
A2._assert("A1-1312       N    10", 3.0)
A3.move("LVL", "M", "H,H,H")
A3._assert("A1-1512       N    10", 3.5)
A4.move("LVL", "M", "H,H,H,H")
A4._assert("A1-1711       N    10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H,H,H")
A1._assert("A1-1110       N    10", 3.0)
A2.move("LVL", "M", "H,H,H")
A2._assert("A1-1309       N    10", 3.5)
A3.move("LVL", "M", "H,H,H,H")
A3._assert("A1-1508       N    10", 4.0)
A4.move("LVL", "M", "H,H,H,H")
A4._assert("A1-1707       N    10", 4.5)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H,H,H")
A1._assert("A1-1107       N    10", 3.0)
A2.move("LVL", "M", "H,H,H")
A2._assert("A1-1306       N    10", 3.5)
A3.move("LVL", "M", "H,H,H,H")
A3._assert("A1-1504       N    10", 4.0)
A4.move("LVL", "M", "H,H,H,H")
A4._assert("A1-1703       N    10", 4.5)
endgameturn()

# SS acceleration and deceleration

starttestsetup(sheets=[["A1"], ["A2"], ["B1"], ["B2"]])
A1 = aircraft("A1", "AF", "F-100A", "A1-2002", "S", 51, 5.5, "CL")
A2 = aircraft("A2", "AF", "F-100A", "A1-2202", "S", 51, 5.5, "CL")
A3 = aircraft("A3", "AF", "F-100A", "A1-2402", "S", 51, 5.5, "CL")
endtestsetup()

startgameturn()
A1.move("SD", "AB", "H,H,H,H,D")
A1._assert("A1-2006       S    50", 5.5)
A2.move("SD", "AB", "H,H,H,H,D")
A2._assert("A1-2206       S    50", 5.5)
A3.move("SD", "AB", "H,H,H,H,D")
A3._assert("A1-2406       S    50", 5.5)
endgameturn()

startgameturn()
A1.move("VD", "AB", "H,H,D3,D3,D3,D3")
A1._assert("A1-2008       S    38", 8.5)
A2.move("VD", "AB", "H,H,D3,D3,D3,D3")
A2._assert("A1-2208       S    38", 8.5)
A3.move("VD", "AB", "H,H,D3,D3,D3,D3")
A3._assert("A1-2408       S    38", 8.5)
endgameturn()

startgameturn()
A1.move("SD", "AB", "H,H,H,H,D2,D2,D2,D2")
A1._assert("A1-2012       S    30", 10.0)
A2.move("SD", "AB", "H,H,H,H,D2,D2,D2,D2")
A2._assert("A1-2212       S    30", 10.0)
A3.move("SD", "AB", "H,H,H,H,D2,D2,D2,D2")
A3._assert("A1-2412       S    30", 10.0)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "H,H,H,H,H,H,H,H,H,H")
A1._assert("A2-2022       S    30", 9.0)
A2.move("LVL", "AB", "H,H,H,H,H,H,H,H,H,H")
A2._assert("A2-2222       S    30", 9.0)
A3.move("LVL", "AB", "H,H,H,H,H,H,H,H,H,H")
A3._assert("A2-2422       S    30", 9.0)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "H,H,H,H,H,H,H,H,H")
A1._assert("A2-2031       S    30", 8.5)
A2.move("LVL", "M", "H,H,H,H,H,H,H,H,H")
A2._assert("A2-2231       S    30", 8.0)
A3.move("LVL", "N", "H,H,H,H,H,H,H,H,H")
A3._assert("A2-2431       S    30", 7.0)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "H,H,H,H,H,H,H,H,H")
A1._assert("B1-4010       S    30", 8.5)
A2.move("LVL", "M", "H,H,H,H,H,H,H,H")
A2._assert("B1-4209       S    30", 7.5)
A3.move("LVL", "N", "H,H,H,H,H,H,H")
A3._assert("B1-4408       S    30", 6.0)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "H,H,H,H,H,H,H,H")
A1._assert("B2-4018       S    30", 8.5)
A2.move("LVL", "M", "H,H,H,H,H,H,H")
A2._assert("B1-4216       S    30", 7.5)
A3.move("LVL", "N", "H,H,H,H,H,H")
A3._assert("B1-4414       S    30", 5.5)
endgameturn()

# Check version 2.4 rules for idle power.

starttestsetup(
    sheets=[["A1"], ["A2"], ["B1"], ["B2"]], variants=["use version 2.4 rules"]
)
A4 = aircraft("A4", "AF", "F-100A", "A1-2602", "S", 51, 5.5, "CL")
endtestsetup()

startgameturn()
A4.move("SD", "AB", "H,H,H,H,D")
A4._assert("A1-2606       S    50", 5.5)
endgameturn()

startgameturn()
A4.move("VD", "AB", "H,H,D3,D3,D3,D3")
A4._assert("A1-2608       S    38", 9.0)
endgameturn()

startgameturn()
A4.move("SD", "AB", "H,H,H,H,D2,D2,D2,D2,D2")
A4._assert("A1-2612       S    28", 10.5)
endgameturn()

startgameturn()
A4.move("LVL", "AB", "H,H,H,H,H,H,H,H,H,H")
A4._assert("A2-2622       S    28", 9.5)
endgameturn()

startgameturn()
A4.move("LVL", "I", "H,H,H,H,H,H,H,H,H,H")
A4._assert("B1-4602       S    28", 6.5)
endgameturn()

startgameturn()
A4.move("LVL", "I", "H,H,H,H,H,H")
A4._assert("B1-4608       S    28", 6.0)
endgameturn()

startgameturn()
A4.move("LVL", "I", "H,H,H,H,H,H")
A4._assert("B1-4614       S    28", 5.0)
endgameturn()

# F-16A is LTD when CL.

starttestsetup(sheets=[["A1"], ["A2"]], variants=["use version 2.4 rules"])
A0 = aircraft("A0", "AF", "F-16A-1", "A1-2402", "S", 10, 6.5, "CL")
A1 = aircraft("A1", "AF", "F-16A-1", "A1-2602", "S", 10, 6.5, "1/2")
A2 = aircraft("A2", "AF", "F-16A-1", "A1-2802", "S", 10, 6.5, "DT")
endtestsetup()

startgameturn()
A0.move("LVL", 2.5, "H,H,H,H,H,H")
A1.move("LVL", 2.5, "H,H,H,H,H,H")
A2.move("LVL", 2.5, "H,H,H,H,H,H")
A0._assert("A1-2408       S    10", 7.0)
A1._assert("A1-2608       S    10", 7.0)
A2._assert("A1-2808       S    10", 7.0)
endgameturn()

startgameturn()
A0.move("LVL", 2.5, "H,H,H,H,H,H,H")
A1.move("LVL", 2.5, "H,H,H,H,H,H,H")
A2.move("LVL", 2.5, "H,H,H,H,H,H,H")
A0._assert("A1-2415       S    10", 7.5)
A1._assert("A1-2615       S    10", 7.0)
A2._assert("A1-2815       S    10", 7.0)
endgameturn()

startgameturn()
A0.move("LVL", 2.5, "H,H,H,H,H,H,H,H")
A1.move("LVL", 2.5, "H,H,H,H,H,H,H")
A2.move("LVL", 2.5, "H,H,H,H,H,H,H")
A0._assert("A2-2423       S    10", 7.5)
A1._assert("A2-2622       S    10", 7.5)
A2._assert("A2-2822       S    10", 7.5)
endgameturn()

endfile(__file__)
