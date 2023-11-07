import apengine                as ap
import apengine._aircraftdata  as apaircraftdata
import apengine._altitude      as apaltitude
import apengine._azimuth       as apazimuth
import apengine._configuration as apconfiguration
import apengine._draw          as apdraw
import apengine._hex           as aphex
import apengine._hexcode       as aphexcode
import apengine._log           as aplog
import apengine._map           as apmap
import apengine._speed         as apspeed
import apengine._stores        as apstores
import apengine._turnrate      as apturnrate

import math
import re

################################################################################

_aircraftlist = []

def _startsetup():
  global _aircraftlist
  global _zorder
  _aircraftlist = []
  _zorder = 0

def _endsetup():
  for a in _aircraftlist:
    a._save(ap.turn())

def _startturn():
  global _zorder
  _zorder = 0
  for a in _aircraftlist:
    a._restore(ap.turn() - 1)
    a._finishedmove = False
    a._startflightpath()
  for a in _aircraftlist:
    a._checkcloseformation()

def _endturn():
  for a in _aircraftlist:
    if not a._destroyed and not a._leftmap and not a._finishedmove:
      raise RuntimeError("aircraft %s has not finished its move." % a._name)
  for a in _aircraftlist:
    a._speed = a._newspeed
    a._newspeed = None
  for a in _aircraftlist:
    a._checkcloseformation()
  for a in _aircraftlist:
    a._save(ap.turn())

def _drawmap():
  for a in _aircraftlist:
    a._drawflightpath()
    a._drawaircraft()

def _fromname(name):
  for a in _aircraftlist:
    if a._name == name:
      return a
  return None

#############################################################################

from ._draw import \
  _zorder

from ._geometry import \
  _showgeometry, _angleofftail, _gunattackrange, _rocketattackrange, _inlimitedradararc

from ._normalflight import \
  _isclimbingflight, _isdivingflight, _islevelflight
    
class aircraft:

  from ._closeformation import \
    joincloseformation, leavecloseformation, \
    _checkcloseformation, _leaveanycloseformation, _breakdowncloseformation, \
    closeformationsize, closeformationnames

  from ._flight import \
    move, continuemove, _endmove

  from ._stalledflight import \
    _checkstalledflight, _dostalledflight

  from ._departedflight import \
    _checkdepartedflight, _dodepartedflight

  from ._normalflight import \
    _checknormalflight, \
    _startnormalflight, _continuenormalflight, _endnormalflight

  from ._specialflight import \
    _checkspecialflight, _dospecialflight

  from ._speed import \
    _startmovespeed, _endmovespeed

  from ._configuration import \
    _updateconfiguration

  from ._damage import \
    damage, _takedamage, takedamage, damageatleast, damageatmost

  from ._flightcapabilities import \
    power, spbr, fuelrate, powerfade, engines, turndrag, \
    minspeed, maxspeed, cruisespeed, climbspeed, maxdivespeed, ceiling, \
    rollhfp, rolldrag, climbcapability, hasproperty, \
    specialclimbcapability, gunarc

  from ._draw import \
    _drawaircraft, \
    _startflightpath, _continueflightpath, _drawflightpath

  from ._log import \
    _log, _logaction, _logstart, _logend, _logevent, _logline, _logbreak, \
    _lognote, _log1, _log2, \
    _logpositionandmaneuver, _logposition

  #############################################################################

  def __init__(self, name, aircrafttype, hexcode, azimuth, altitude, speed,
    configuration="CL",
    fuel=None, bingofuel=None, 
    gunammunition=None, rocketfactors=None, stores=None, 
    color="unpainted", counter=False
  ):

    global _aircraftlist

    aplog.clearerror()
    try:

      if not isinstance(name, str):
        raise RuntimeError("the name argument must be a string.")
      for a in _aircraftlist:
        if name == a._name:
          raise RuntimeError("the name argument must be unique.")

      if not isinstance(aircrafttype, str):
        raise RuntimeError("the aircrafttype argument must be a string.")
      # Require the hexcode to be a string to avoid surprised with things like 2020/2120 rather than "2020/2120".
      if not isinstance(hexcode, str):
        raise RuntimeError("the hexcode argument must be a string.")
      if not aphexcode.isvalidhexcode(hexcode):
        raise RuntimeError("the hexcode argument is not valid.")
      if not apazimuth.isvalidazimuth(azimuth):
        raise RuntimeError("the azimuth argument is not valid.")
      if not apaltitude.isvalidaltitude(altitude):
        raise RuntimeError("the altitude argument is not valid.")
      if not apspeed.isvalidspeed(speed):
        raise RuntimeError("the speed argument is not valid.")
      if not apconfiguration.isvalidconfiguration(configuration):
        raise RuntimeError("the configuration argument is not valid.")

      x, y = aphexcode.toxy(hexcode)
      facing = apazimuth.tofacing(azimuth)
      if not aphex.isvalid(x, y, facing):
        raise RuntimeError("the combination of hexcode and facing are not valid.")

      # In addition to the specified position, azimuth, altitude, speed, and 
      # configuration, aircraft initially have level flight, normal power, and
      # no carries.

      self._logbreak()
      self._logline()
      self._name                  = name
      self._logaction("", "creating aircraft %s." % name)

      self._x                     = x
      self._y                     = y
      self._facing                = facing
      self._altitude              = altitude
      self._altitudeband          = apaltitude.altitudeband(self._altitude)
      self._altitudecarry         = 0
      self._speed                 = speed
      self._newspeed              = None
      self._damageL               = 0
      self._damageH               = 0
      self._damageC               = 0
      self._damageK               = 0
      self._flighttype            = "LVL"
      self._powersetting          = "N"
      self._bank                  = None
      self._maneuvertype          = None
      self._maneuversense         = None
      self._maneuverfp            = 0
      self._maneuverrequiredfp    = 0
      self._maneuverfacingchange  = None
      self._manueversupersonic    = False
      self._wasrollingonlastfp    = False
      self._fpcarry               = 0
      self._apcarry               = 0
      self._gloccheck             = 0
      self._closeformation        = []
      self._aircraftdata          = apaircraftdata.aircraftdata(aircrafttype)
      if gunammunition is None:
        self._gunammunition       = self._aircraftdata.gunammunition()
      else:
        self._gunammunition       = gunammunition
      if rocketfactors is None:
        self._rocketfactors       = self._aircraftdata.rocketfactors()
      else:
        self._rocketfactors       = rocketfactors
      self._destroyed             = False
      self._leftmap               = False
      self._turnsstalled          = 0
      self._turnsdeparted         = 0
      self._finishedmove          = True
      self._flightpathx           = []
      self._flightpathy           = []
      self._color                 = color
      self._counter               = counter

      self._logaction("", "type          is %s." % aircrafttype)
      self._logaction("", "position      is %s." % self.position())
      self._logaction("", "speed         is %.1f." % self._speed)

      # Determine the fuel and bingo levels.
    
      if isinstance(fuel, str) and fuel[-1] == "%" and fuel[:-1].isdecimal():
        fuel = float(fuel[:-1]) / 100
        self._logaction("", "fuel          is %3.0f%% of internal capacity." % (fuel * 100))
        fuel *= self.internalfuelcapacity()
      elif fuel is not None and not isinstance(fuel, int|float):
        raise RuntimeError("invalid fuel value %r" % fuel)
      self._fuel = fuel

      if isinstance(bingofuel, str) and bingofuel[-1] == "%" and bingofuel[:-1].isdecimal():
        bingofuel = float(bingofuel[:-1]) / 100 
        self._logaction("", "bingo fuel    is %3.0f%% of internal capacity." % (bingofuel * 100))
        bingofuel *= self.internalfuelcapacity()
      elif bingofuel is not None and not isinstance(bingofuel, int|float):
        raise RuntimeError("invalid bingo fuel value %r" % bingofuel)
      self._bingofuel = bingofuel

      if not self._fuel is None:
        if self._bingofuel is None:
          self._logaction("", "fuel          is %.1f." % self._fuel)
        else:
          self._logaction("", "fuel          is %.1f and bingo fuel is %.1f." % (self._fuel, self._bingofuel)) 

      # Determine the configuration, either explicitly or from the specified
      # stores.

      if stores is None:

        self._stores        = stores
        self._configuration = configuration

      else:

        self._stores = apstores._checkstores(stores)
        if len(self._stores) != 0:
          apstores._showstores(stores, 
            printer=lambda s: self._logaction("", s), 
            fuel=self.externalfuel())

        if self.fuel() is not None and self.fuel() > self.internalfuelcapacity() + self.externalfuelcapacity():
          raise RuntimeError("total fuel exceeds the internal and external capacity.")

      self._updateconfiguration()
      self._logaction("", "configuration is %s." % self._configuration)

      global _zorder
      _zorder += 1
      self._zorder = _zorder
    
      self._saved = []

      _aircraftlist.append(self)
      
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  #############################################################################

  def __str__(self):

    s = ""
    for x in [
      ["name"         , self._name],
      ["sheet"        , apmap.tosheet(self._x, self._y) if not self._leftmap else "-- "],
      ["hexcode"      , aphexcode.fromxy(self._x, self._y) if not self._leftmap else "----"],
      ["facing"       , apazimuth.fromfacing(self._facing)],
      ["speed"        , self._speed],
      ["altitude"     , self._altitude],
      ["altitudeband" , self._altitudeband],
      ["flighttype"   , self._flighttype],
      ["powersetting" , self._powersetting],
      ["configuration", self._configuration],
      ["fpcarry"      , self._fpcarry],
      ["apcarry"      , self._apcarry],
      ["gloccheck"    , self._gloccheck],
      ["altitudecarry", self._altitudecarry],
      ["destroyed"    , self._destroyed],
      ["leftmap"      , self._leftmap],
    ]:
      s += "%-16s: %s\n" % (x[0], x[1])
    return s

  #############################################################################

  def position(self):

    if apmap.isonmap(self._x, self._y):
      hexcode = aphexcode.fromxy(self._x, self._y)
    else:
      hexcode = "----"
    azimuth = apazimuth.fromfacing(self._facing)
    altitude = self._altitude
    return "%-9s  %-3s  %2d" % (hexcode, azimuth, altitude)

  #############################################################################

  def maneuver(self):
    if self._maneuverfacingchange == 60 or self._maneuverfacingchange == 90:
      return "%s%s %d/%d %d" % (self._maneuvertype, self._maneuversense, self._maneuverfp, self._maneuverrequiredfp, self._maneuverfacingchange)
    elif self._maneuvertype != None:
      return "%s%s %d/%d" % (self._maneuvertype, self._maneuversense, self._maneuverfp, self._maneuverrequiredfp)
    elif self._bank != None:
      return "BK%s" % self._bank
    else:
      return "WL"

  #############################################################################

  def note(self, s):
    self._lognote(s)
    self._logline()

  #############################################################################

  def react(self, action, note=False):

    """
    Return fire, either with fixed guns or articulated guns.
    """

    aplog.clearerror()
    try:

      ap._checkinturn()
      self._logaction("react", action)

      m = re.compile("AA" + 3 * r"\(([^)]*)\)").match(action)
      if m is None:
        raise RuntimeError("invalid action %r" % action)

      weapon     = m[1]
      targetname = m[2]
      result     = m[3]

      if weapon == "GN":
        weaponname = "gun"
        if self._gunammunition < 1.0:
          raise RuntimeError("gun ammunition is %d." % self._gunammunition)
        self._gunammunition -= 1.0
      elif weapon == "SSGN":
        weaponname = "snap-shot gun"
        if self._gunammunition < 0.5:
          raise RuntimeError("gun ammunition is %d." % self._gunammunition)
        self._gunammunition -= 0.5
      else:
        raise RuntimeError("invalid weapon %r." % weapon)

      if targetname == "":
        self._logevent("%s air-to-air attack." % weaponname)
      else:
        target = _fromname(targetname)
        if target == None:
          raise RuntimeError("unknown target aircraft %s." % targetname)
        self._logevent("%s air-to-air attack on %s." % (weaponname, targetname))

      if self.gunarc() != None:
        self._logevent("gunnery arc is %s." % self.gunarc())

      if targetname != "":
        r = self.gunattackrange(target, arc=self.gunarc())
        if isinstance(r, str):
            raise RuntimeError(r)      
        self._logevent("range is %d." % r)      
        self._logevent("angle-off-tail is %s." % self.angleofftail(target))

      if result == "":
        self._logevent("result of attack not specified.")
      elif result == "M":
        self._logevent("missed.")
      elif result == "-":
        self._logevent("hit but inflicted no damage.")
      else:
        self._logevent("hit and inflicted %s damage." % result)
        if target != None:
          target._takedamage(result)

      if weapon == "GN" or weapon == "SSGN":
        self._logevent("gun ammunition is now %.1f." % self._gunammunition)
      
      self._lognote(note)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)
    
  #############################################################################

  def angleofftail(self, other):

    """
    Return the angle of the aircraft off the tail of the other aircraft.
    """

    return _angleofftail(self, other)

  #############################################################################

  def gunattackrange(self, other, arc=False):

    """
    Return the gun attack range of the other aircraft from the aircraft
    or a string explaining why it cannot be attacked.
    """

    return _gunattackrange(self, other, arc=arc)

  #############################################################################

  def rocketattackrange(self, other):

    """
    Return the rocket attack range of the other aircraft from the aircraft
    or a string explaining why it cannot be attacked.
    """

    return _rocketattackrange(self, other)

  #############################################################################

  def inlimitedradararc(self, other):

    """
    Return True if the other aircraft is in the limited radar arc of the aircraft.
    """

    return _inlimitedradararc(self, other)
    
  #############################################################################

  def fuel(self):
    return self._fuel

  def internalfuel(self):
    if self.fuel() is None:
      return None
    else:
      return min(self.fuel(), self.internalfuelcapacity())

  def externalfuel(self):
    if self.fuel() is None:
      return None
    else:
      return max(0, self.fuel() - self.internalfuelcapacity())

  def externalfuelcapacity(self):
    return apstores.totalfuelcapacity(self._stores)

  def internalfuelcapacity(self):
    return self._aircraftdata.fuel()

  #############################################################################

  def showstores(self, note=False):
    """
    Show the aircraft's stores.
    """

    aplog.clearerror()
    try:

      ap._checkinsetuporturn()
      self._logbreak()
      self._logline()

      apstores._showstores(self._stores, 
        printer=lambda s: self._log(s),
        fuel=self.externalfuel())
  
      self._lognote(note)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  #############################################################################
  
  def showgeometry(self, other, note=False):

    """
    Show the geometry of the other aircraft with respect to the aircraft.
    """

    aplog.clearerror()
    try:

      ap._checkinsetuporturn()
      self._logbreak()
      self._logline()

      _showgeometry(self, other)
  
      self._lognote(note)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)
      
  #############################################################################

  def climbingflight(self):

    """
    Return true if the aircraft is climbing.
    """

    return _isclimbingflight(self._flighttype)

  #############################################################################

  def divingflight(self):

    """
    Return true if the aircraft is diving.
    """

    return _isdivingflight(self._flighttype)
   
  #############################################################################

  def levelflight(self):

    """
    Return true if the aircraft is in level flight.
    """

    return _islevelflight(self._flighttype)
    
  #############################################################################

  def checkforterraincollision(self):

    """
    Check if the aircraft has collided with terrain.
    """

    altitudeofterrain = apaltitude.terrainaltitude(self._x, self._y)
    if self._altitude <= altitudeofterrain:
      self._altitude = altitudeofterrain
      self._altitudecarry = 0
      self._logaction("", "aircraft has collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True
      self._leaveanycloseformation()

  def checkforleavingmap(self):

    """
    Check if the aircraft has left the map.
    """

    if not apmap.isonmap(self._x, self._y):
      self._logaction("", "aircraft has left the map.")
      self._leftmap = True
      self._leaveanycloseformation()
  
  ##############################################################################

  # Turn management
  
  def _restore(self, i):

    """
    Restore the aircraft properties at the start of the specified turn.
    """

    self._x, \
    self._y, \
    self._facing, \
    self._altitude, \
    self._altitudecarry, \
    self._speed, \
    self._configuration, \
    self._gunammunition, \
    self._fuel, \
    self._damageL, \
    self._damageH, \
    self._damageC, \
    self._damageK, \
    self._powersetting, \
    self._flighttype, \
    self._bank, \
    self._maneuvertype, \
    self._maneuversense, \
    self._maneuverfp, \
    self._maneuverrequiredfp, \
    self._maneuverfacingchange, \
    self._manueversupersonic, \
    self._wasrollingonlastfp, \
    self._fpcarry, \
    self._apcarry, \
    self._gloccheck, \
    self._closeformation, \
    self._destroyed, \
    self._leftmap, \
    self._turnsstalled, \
    self._turnsdeparted \
    = self._saved[i]
    self._altitudeband = apaltitude.altitudeband(self._altitude)

  def _save(self, i):

    """
    Save the aircraft properties at the end of the specified turn.
    """

    if len(self._saved) == i:
      self._saved.append(None)
    self._saved[i] = ( \
      self._x, \
      self._y, \
      self._facing, \
      self._altitude, \
      self._altitudecarry, \
      self._speed, \
      self._configuration, \
      self._gunammunition, \
      self._fuel, \
      self._damageL, \
      self._damageH, \
      self._damageC, \
      self._damageK, \
      self._powersetting, \
      self._flighttype, \
      self._bank, \
      self._maneuvertype, \
      self._maneuversense, \
      self._maneuverfp, \
      self._maneuverrequiredfp, \
      self._maneuverfacingchange, \
      self._manueversupersonic, \
      self._wasrollingonlastfp, \
      self._fpcarry, \
      self._apcarry, \
      self._gloccheck, \
      self._closeformation, \
      self._destroyed, \
      self._leftmap, \
      self._turnsstalled, \
      self._turnsdeparted \
    )

 ################################################################################

  def hasbeenkilled(self):
    ap._checkinturn()
    self._log("has been killed.")
    self._destroyed = True

  ################################################################################

  def _assert(self, position, speed, configuration=None):

    """
    Verify the position and new speed of an aircraft.
    """

    if aplog._error != None:
      print("== assertion failed ===")
      print("== unexpected error: %r" % aplog._error)
      assert aplog._error == None
    if position != None and position != self.position():
      print("== assertion failed ===")
      print("== actual position  : %s" % self.position())
      print("== expected position: %s" % position)
      assert position == self.position()
    if speed is not None:
      if self._newspeed is None:
        if speed != self._speed:
          print("== assertion failed ===")
          print("== actual   speed: %.1f" % self._speed)
          print("== expected speed: %.1f" % speed)
          assert speed == self._speed
      else:
        if speed != self._newspeed:
          print("== assertion failed ===")
          print("== actual   new speed: %.1f" % self._newspeed)
          print("== expected new speed: %.1f" % speed)
          assert speed == self._newspeed
    if configuration != None and configuration != self._configuration:
      print("== assertion failed ===")
      print("== actual speed  : %s" % self._configuration)
      print("== expected speed: %s" % configuration)
      assert configuration == self._configuration

  ################################################################################  
