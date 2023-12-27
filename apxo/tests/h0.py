from apxo.tests.infrastructure import *
startfile(__file__, "stores")

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "1": "FT/600L",
                "4": "FT/600L",
                "2": "BB/M65",
                "3": "BB/M65"
              })
A1._assert("A2-2024       N    10", 4.0, expectedconfiguration="DT")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "1": "FT/600L",
                "4": "FT/600L",
              })
A1._assert("A2-2024       N    10", 4.0, expectedconfiguration="1/2")
endtestsetup()


starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "5": "RK/HVAR",
                "8": "RK/HVAR",
              })
A1._assert("A2-2024       N    10", 4.0, expectedconfiguration="CL")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "3": "BB/M57",
                "4": "BB/M57"
              })
A1._assert("A2-2024       N    10", 4.0, expectedconfiguration="CL")
endtestsetup()

# Check effect of external fuel on load. An F-104A can have 2 points on
# its central load point and still be clean. A FT/600L has 2 points when
# empty and 3 points when full.

starttestsetup()
A1 = aircraft("A1", "AF", "F-104A", "2024", "N", 10, 4.0, fuel="100%",
              stores={
                "3": "FT/600L",
              })
A1._assert("A2-2024       N    10", 4.0, expectedconfiguration="CL")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "AF", "F-104A", "2024", "N", 10, 4.0, fuel="101%",
              stores={
                "3": "FT/600L",
              })
A1._assert("A2-2024       N    10", 4.0, expectedconfiguration="1/2")
endtestsetup()

# Check expectedconfiguration changes when we exhaust external fuel.

startturn()
A1.move("LVL", "AB", "H,H,H,H")
A1._assert("A2-2020       N    10", 4.5, expectedconfiguration="CL")
endturn()

# Check jettisoning.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "1": "FT/600L",
                "4": "FT/600L",
                "2": "BB/M57",
                "3": "BB/M57"
              })
A1._assert("A2-2024       N    10", 4.0, expectedconfiguration="DT")
endtestsetup()

startturn()
A1.move("LVL", "N", "H/J(BB),H,H,H")
A1._assert("A2-2020       N    10", 4.0, expectedconfiguration="1/2")
endturn()

startturn()
A1.move("LVL", "N", "H/J(1+4),H,H,H")
A1._assert("A1-2016       N    10", 4.0, expectedconfiguration="CL")
endturn()


endfile(__file__)