from apxo.tests.infrastructure import *

startfile(__file__, "air-to-air attacks")

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-80C", "A2-2025", "N", 5, 4.0, "CL")
A2 = aircraft("A2", "AF", "Tu-4", "A2-2023", "E", 5, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C", "A2-2025", "N", 5, 4.0, "CL", gunammunition=3.5)
A4 = aircraft("A4", "AF", "Tu-4", "A2-2023", "E", 5, 4.0, "CL", gunammunition=11.0)
A5 = aircraft("A5", "AF", "F-89D", "A2-2023", "E", 5, 4.0, "CL")
A6 = aircraft("A6", "AF", "F-102A", "A2-2023", "E", 5, 4.0, "CL", rocketfactors=0)
A7 = aircraft("A7", "AF", "F-100C", "A2-2025", "N", 5, 6.0, "CL")
A8 = aircraft("A8", "AF", "Tu-4", "A2-2023", "N", 5, 4.0, "CL")
endtestsetup()

startgameturn()

A1.move("LVL", "M", "TTR/H")
A1.attackaircraft("GN", A2, "L")
A2.react("AA(GN)(A1)(L)")
A1.continuemove("H")
A1.attackaircraft("GN/SS", A2, "M")
A2.react("AA(GN/SS)(A1)(L)")
A1.continuemove("H,H")
A2.move("LVL", "N", "H,H,H,H")
A1._assert("A2-2021       N     5", 4.0)
A2._assert("A2-2423       E     5", 3.5)
assert A1._gunammunition == 6.5
assert A2._gunammunition == 18.5

assert A3._gunammunition == 3.5
A3.move("LVL", "M", "H")
A3.attackaircraft("GN", A4, "A")
assert A3._gunammunition == 3.5
A3.continuemove("H")
A3.attackaircraft("GN", A4, "-")
assert A3._gunammunition == 2.5

assert A4._gunammunition == 11.0

assert A5._rocketfactors == 9
A5.move("LVL", "M", "H")
A5.attackaircraft("RK/3", A2, "A")
assert A5._rocketfactors == 9
A5.continuemove("H")
A5.attackaircraft("RK/3", A2, "-")
assert A5._rocketfactors == 6

assert A6._rocketfactors == 0

# Check SSGT and RR

startgameturn()
A7.move("LVL", "M", "H")
A7.attackaircraft("GN/RR", A8, "-")
asserterror("RE radar-ranging requires SSGT.")
startgameturn()
A7.move("LVL", "M")
A7.ssgt(A8)
A7.continuemove("H")
A7.attackaircraft("GN/RR", A8, "-")
assert A7._gunammunition == 3.0
startgameturn()
A7.move("LVL", "M")
A7.ssgt(A8)
A7.continuemove("H")
A7.attackaircraft("GN/SS/RR", A8, "-")
assert A7._gunammunition == 3.5
startgameturn()
A7.move("LVL", "M")
A7.ssgt(A8)
A7.continuemove("H")
A7.attackaircraft("GN/SS/RR", A8, "-")
assert A7._gunammunition == 3.5

# Check CC
startgameturn()
A2.move("LVL", "N", "H,H,H,H")
A5.move("LVL", "M", "H")
A5.attackaircraft("RK/3/CC", A2, "-")
assert A5._rocketfactors == 6

# Check recovery after ET.

startgameturn()
A7.move("LVL", "M", "ETR/H")
A7.attackaircraft("GN")
asserterror("attempt to use weapons while in an ET.")
startgameturn()
A7.move("LVL", "M", "ETR/HR,H")
A7.attackaircraft("GN")
asserterror("attempt to use weapons while recovering from an ET.")
startgameturn()
A7.move("LVL", "M", "ETR/HR,H,H")
A7.attackaircraft("GN")
asserterror("attempt to use weapons while recovering from an ET.")
startgameturn()
A7.move("LVL", "M", "ETR/HR,H,H,H")
A7.attackaircraft("GN")
asserterror("attempt to use weapons while recovering from an ET.")
startgameturn()
A7.move("LVL", "M", "ETR/HR,H,H,H,H")
A7.attackaircraft("GN")
A7._assert("A2-2221       NNE   5", 6.0)

# Check error if attack results are not specified at end of turn.
starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A2-2025", "N", 5, 4.0, "CL")
A2 = aircraft("A2", "AF", "Tu-4", "A2-2024", "N", 5, 3.0, "CL")
endtestsetup()

startgameturn()
A2.move("LVL", "FT", "H,H,H")
A1.move("LVL", "M", "H,H,H,H")
A1.attackaircraft("GN", A2)
endgameturn()
asserterror("aircraft A1 has 1 unspecified attack result.")

startgameturn()
A2.move("LVL", "FT", "H,H,H")
A1.move("LVL", "M", "H,H,H")
A1.attackaircraft("GN", A2)
A1.continuemove("H")
A1.attackaircraft("GN", A2)
endgameturn()
asserterror("aircraft A1 has 2 unspecified attack results.")

# Check SSGT

starttestsetup()
A0 = aircraft("A0", "AF", "F-80C", "A1-1815", "N", 20, 4.0, "CL")
A1 = aircraft("A1", "AF", "F-80C", "A1-1814", "N", 20, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C", "A1-2212", "WNW", 20, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C", "A1-2210", "W", 20, 4.0, "CL")
A4 = aircraft("A4", "AF", "F-80C", "A1-1810", "N", 20, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "H,H,H,H")
A0.move("LVL", "M", "SSGT(A1)/H,H,H,H/AA(GN)(A1)(-)")

startgameturn()
A2.move("LVL", "M", "H,H,H,H")
A0.move("LVL", "M", "SSGT(A2)/H,H,H,H/AA(GN)(A2)(-)")

startgameturn()
A3.move("LVL", "M", "H,H,H,H")
A0.move("LVL", "M")
A0.ssgt(A3)
asserterror("attempt to start SSGT while A0 is not in its 60- arc of A3.")

startgameturn()
A4.move("LVL", "M", "H,H,H,H")
A0.move("LVL", "M")
A0.ssgt(A4)
asserterror("attempt to start SSGT while A4 is more than 6 hexes from A0.")

startgameturn()
A1.move("LVL", "M", "H,H,H,H")
A0.move("LVL", "M")
A0.ssgt(A1)
A0.continuemove("BTR/H/R,H/WL,BTL/H/L+,H/L")
A0.attackaircraft("GN", A1, "-")
