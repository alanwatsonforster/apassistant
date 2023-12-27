from apxo.tests.infrastructure import *
startfile(__file__, "stalled flight")

# Stalled flight

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-80C", "A1-1914", "N", 10, 1.0, configuration="DT")
A2 = aircraft("A2", "AF", "F-80C", "A1-2114", "N",  3, 1.0, configuration="DT")
A3 = aircraft("A3", "AF", "F-80C", "A1-2314", "N",  2, 1.0, configuration="DT")
endtestsetup()

startturn()
A1.move("ST", "M", "")
A1._assert("A1-1914       N     9", 1.0)
A2.move("ST", "M", "")
A2._assert("A1-2114       N     2", 1.0)
A3.move("ST", "M", "")
A3._assert("A1-2314       N     1", 1.0)
endturn()

startturn()
A1.move("ST", "M", "")
A1._assert("A1-1914       N     7", 2.0)
A2.move("ST", "M", "")
A2._assert("A1-2114       N     0", 1.0)
A3.move("ST", "M", "")
A3._assert("A1-2314       N     0", 1.0)
endturn()

startturn()
A1.move("LVL", "M", "H,H")
A1._assert("A1-1912       N     7", 2.0)
endturn()

# Check jettisoning.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A2-2024", "N", 10, 1.0,
              stores={
                "1": "FT/600L",
                "4": "FT/600L",
                "2": "BB/M57",
                "3": "BB/M57"
              })
A1._assert("A2-2024       N    10", 1.0, expectedconfiguration="DT")
endtestsetup()

startturn()
A1.move("ST", "N", "J(BB)")
A1._assert("A2-2024       N     9", 1.0, expectedconfiguration="1/2")
endturn()

startturn()
A1.move("ST", "N", "J(1+4)")
A1._assert("A2-2024       N     7", 1.5, expectedconfiguration="CL")
endturn()


endfile(__file__)