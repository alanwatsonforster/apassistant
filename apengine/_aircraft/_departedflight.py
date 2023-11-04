"""
Departed flight for the aircraft class.
"""

import math

import apengine._altitude as apaltitude
import apengine._hex      as aphex

def _checkdepartedflight(self):

  """
  Check departed flight is allowed.
  """

  if self.hasproperty("SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform departed flight.")

def _dodepartedflight(self, action):

  """
  Carry out departed flight.
  """

  self._logline()
  self._logaction("start", "", self.position())   

  # See rule 6.4 "Abnormal FLight (Stalls and Departures)" and rule 7.7 
  # "Manuevering Departures".
      
  # The action specifies a possible shift and the facing change. Valid values 
  # are:
  #
  # - "R30", "R60", "R90", ..., "R300"
  # - "R", "RR", and "RRR" which as usual mean "R30", "R60", and "R90"
  # - the "L" equivalents.

  if action[0:2] == "MD":
    maneuveringdeparture = True
    action = action[2:]
  else:
    maneuveringdeparture = False

  if action == "R":
    action = "R30"
  elif action == "RR":
    action = "R60"
  elif action == "RRR":
    action = "R90"
  elif action == "L":
    action = "L30"
  elif action == "LL":
    action = "L60"
  elif action == "LLL":
    action = "L90"
  
  if len(action) < 3 or (action[0] != "R" and action[0] != "L") or not action[1:].isdecimal():
    raise RuntimeError("invalid action %r for departed flight." % action)

  sense = action[0]
  facingchange = int(action[1:])
  if facingchange % 30 != 0 or facingchange <= 0 or facingchange > 300:
    raise RuntimeError("invalid action %r for departed flight." % action)

  if maneuveringdeparture:

      # Do the first facing change.

      if aphex.isedge(self._x, self._y):
        self._x, self._y = aphex.centertoright(self._x, self._y, self._facing, sense)
      if action[0] == "L":
        self._facing = (self._facing + 30) % 360
      else:
        self._facing = (self._facing - 30) % 360
      self._continueflightpath()
      facingchange -= 30

      # Shift.

      # See rule 5.4.
      self._maxfp = self._speed + self._fpcarry
      self._fpcarry = 0

      shift = int((self._maxfp) / 2)
      for i in range(0, shift):
        self._x, self._y = aphex.forward(self._x, self._y, self._facing)
        self.checkforterraincollision()
        self.checkforleavingmap()
        if self._destroyed or self._leftmap:
          return

   # Do the (remaining) facing change.

  if aphex.isedge(self._x, self._y):
    self._x, self._y = aphex.edgetocenter(self._x, self._y, self._facing, sense)
  if action[0] == "L":
    self._facing = (self._facing + facingchange) % 360
  else:
    self._facing = (self._facing - facingchange) % 360
  self._continueflightpath()

  # Now lose altitude.

  initialaltitudeband = self._altitudeband
  altitudechange = math.ceil(self._speed + 2 * self._turnsdeparted)
  self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
  self._altitudeband = apaltitude.altitudeband(self._altitude)
  
  self._logaction("end", action, self.position())
  if initialaltitudeband != self._altitudeband:
    self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
  self.checkforterraincollision()

  self._newspeed = self._speed

  self._logline()

