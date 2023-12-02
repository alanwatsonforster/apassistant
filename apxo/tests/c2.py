from apxo.tests.infrastructure import *
startfile(__file__, "flamed-out engines")

# Power with Flamed-Out Engines.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "1330", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C", "1530", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F7U-3", "1730", "N", 10, 4.0, "CL")
A4 = aircraft("A4", "AF", "F7U-3", "1930", "N", 10, 4.0, "CL")
A5 = aircraft("A5", "AF", "F7U-3", "2130", "N", 10, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "M", "H,H,H,H")
A1._assert("1326       N    10",  4.0)
A2.move("LVL", "M", "H,H,H", flamedoutengines=1)
A2._assert("1527       N    10", 3.5)
A3.move("LVL",  "AB", "H,H,H,H")
A3._assert("1726       N    10",  4.0)
A4.move("LVL", "AB", "H,H,H,H", flamedoutengines=1)
A4._assert("1926       N    10", 4.0)
A5.move("LVL", "AB", "H,H,H", flamedoutengines=2)
A5._assert("2127       N    10", 3.5)
endturn()

startturn()
A1.move("LVL",  "M", "H,H,H,H")
A1._assert("1322       N    10",  4.5)
A2.move("LVL", "M", "H,H,H", flamedoutengines=1)
A2._assert("1524       N    10", 3.0)
A3.move("LVL",  "AB", "H,H,H,H")
A3._assert("1722       N    10",  4.5)
A4.move("LVL", "AB", "H,H,H,H", flamedoutengines=1)
A4._assert("1922       N    10", 4.0)
A5.move("LVL", "AB", "H,H,H", flamedoutengines=2)
A5._assert("2124       N    10", 3.0)
endturn()

startturn()
A1.move("LVL",  "M", "H,H,H,H")
A1._assert("1318       N    10",  4.5)
A2.move("LVL", "M", "H,H,H", flamedoutengines=1)
A2._assert("1521       N    10", 2.5)
A3.move("LVL",  "AB", "H,H,H,H")
A3._assert("1718       N    10",  5.0)
A4.move("LVL", "AB", "H,H,H,H", flamedoutengines=1)
A4._assert("1918       N    10", 4.5)
A5.move("LVL", "AB", "H,H,H", flamedoutengines=2)
A5._assert("2121       N    10", 2.5)
endturn()

startturn()
A1.move("LVL",  "M", "H,H,H,H,H")
A1._assert("1313       N    10",  5.0)
A2.move("LVL", "M", "H,H", flamedoutengines=1)
A2._assert("1519       N    10", 2.0)
A3.move("LVL",  "AB", "H,H,H,H,H")
A3._assert("1713       N    10",  5.5)
A4.move("LVL", "AB", "H,H,H,H", flamedoutengines=1)
A4._assert("1914       N    10", 4.5)
A5.move("LVL", "AB", "H,H", flamedoutengines=2)
A5._assert("2119       N    10", 2.0)
endturn()

# Flame-Out Warnings

# We don't automatically check that the warnings are issued, but if the code is run with verbose=True they should appear.

starttestsetup(sheets=[["A1"],["A2"]], verbose=False)
A1 = aircraft("A1", "AF", "F-80C", "1330", "N", 45, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C", "1530", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F7U-3", "1730", "N", 10, 4.0, "CL")
endtestsetup()

startturn()
A1.move("ZC",  "M", "H,H,H,C")
A1._assert("1327       N    46",  4.0)
A2.move("DP",  "M", "R180")
A2._assert("1530       S     6",  4.0)
A3.move("LVL",  "I", "H,H,H")
A3._assert("1727       N    10",  3.5)
endturn()

startturn()
A1.move("ZC",  "M", "H,H,H,C")
A1._assert("1324       N    47",  4.0)
A2.move("DP",  "M", "R180")
A2._assert("1530       N     0",  4.0)
A3.move("LVL",  "AB", "H,H,H,H")
A3._assert("1723       N    10",  3.5)
endturn()

endfile(__file__)