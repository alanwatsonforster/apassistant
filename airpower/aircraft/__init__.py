import airpower.aircrafttype as apaircrafttype
import airpower.altitude     as apaltitude
import airpower.azimuth      as apazimuth
import airpower.data         as apdata
import airpower.draw         as apdraw
import airpower.hex          as aphex
import airpower.hexcode      as aphexcode
import airpower.log          as aplog
import airpower.map          as apmap
import airpower.turn         as apturn

import math

from ._normalflight import _isdiving, _isclimbing
    
class aircraft:

  from ._departedflight import _dodepartedflight
  from ._draw           import _drawaircraft, _drawflightpath
  from ._log            import _log, _logposition, _logevent, _logbreak
  from ._normalflight   import \
    _startnormalflight, _continuenormalflight, \
    _doaction, _doelements, _getelementdispatchlist, \
    _doattack, _doclimb, _dodive, _dohorizontal, _dojettison, _dokilled, \
    _dobank, _dodeclareturn, _doturn, _dospeedbrakes
  from ._speed          import _startmovespeed, _endmovespeed
  from ._stalledflight  import _dostalledflight

  #############################################################################

  def __init__(self, name, aircrafttype, hexcode, azimuth, altitude, speed, configuration="CL"):

    aplog.clearerror()
    try:

      x, y = aphexcode.toxy(hexcode)
      facing = apazimuth.tofacing(azimuth)

      apaltitude.checkisvalidaltitude(altitude)
      aphex.checkisvalidfacing(x, y, facing)

      # In addition to the specified position, azimuth, altitude, speed, and 
      # configuration, aircraft initially have level flight, normal power, and
      # no carries.

      self._name          = name
      self._x             = x
      self._y             = y
      self._facing        = facing
      self._altitude      = altitude
      self._altitudeband  = apaltitude.altitudeband(self._altitude)
      self._altitudecarry = 0
      self._speed         = speed
      self._configuration = configuration
      self._flighttype    = "LVL"
      self._powersetting  = "N"
      self._bank          = None
      self._turnrate      = None
      self._turnfp        = 0
      self._fpcarry       = 0
      self._apcarry       = 0
      self._aircrafttype  = apaircrafttype.aircrafttype(aircrafttype)
      self._destroyed     = False
      self._leftmap       = False
      self._turnsstalled  = 0
      self._turnsdeparted = 0

      self._saved = []
      self._save(0)

      self._drawaircraft("end")

    except RuntimeError as e:
      aplog.logerror(e)

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
      ["altitudecarry", self._altitudecarry],
      ["destroyed"    , self._destroyed],
      ["leftmap"      , self._leftmap],
    ]:
      s += "%-16s: %s\n" % (x[0], x[1])
    return s

  #############################################################################

  def position(self):

    if apmap.isonmap(self._x, self._y):
      sheet = apmap.tosheet(self._x, self._y)
      hexcode = aphexcode.fromxy(self._x, self._y)
    else:
      sheet = "--"
      hexcode = "----"
    azimuth = apazimuth.fromfacing(self._facing)
    altitude = self._altitude
    altitudeband = self._altitudeband
    return "%2s %-9s  %-3s  %2d  %2s" % (sheet, hexcode, azimuth, altitude, altitudeband)

  #############################################################################

  def checkforterraincollision(self):

    """
    Check if the aircraft has collided with terrain.
    """

    altitudeofterrain = apaltitude.terrainaltitude()
    if self._altitude <= altitudeofterrain:
      self._altitude = altitudeofterrain
      self._altitudecarry = 0
      self._logevent("aircraft has collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True

  def checkforleavingmap(self):

    """
    Check if the aircraft has left the map.
    """

    if not apmap.iswithinmap(self._x, self._y):
      self._logevent("aircraft has left the map.")
      self._leftmap = True
  
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
    self._powersetting, \
    self._flighttype, \
    self._bank, \
    self._turnrate, \
    self._turnfp, \
    self._fpcarry, \
    self._apcarry, \
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
      self._powersetting, \
      self._flighttype, \
      self._bank, \
      self._turnrate, \
      self._turnfp, \
      self._fpcarry, \
      self._apcarry, \
      self._destroyed, \
      self._leftmap, \
      self._turnsstalled, \
      self._turnsdeparted \
    )

  ##############################################################################

  def _checkflighttype(self):

    """
    Check the flight type at the start of a move.
    """

    flighttype     = self._flighttype
    lastflighttype = self._lastflighttype

    if flighttype not in ["LVL", "SC", "ZC", "VC", "SD", "UD", "VD", "ST", "DP"]:
      raise RuntimeError("invalid flight type %r." % flighttype)

    self._log("flight type is %s." % flighttype)

    minspeed = self._aircrafttype.minspeed(self._configuration, self._altitudeband)

    if lastflighttype == "DP" and flighttype != "DP":

      # See rule 6.4.

      if _isclimbing(flighttype):
        raise RuntimeError("flight type immediately after DP must not be climbing.")
      elif flighttype == "LVL" and not self._aircrafttype.hasproperty("HPR"):
        raise RuntimeError("flight type immediately after DP must not be level.")

    elif self._speed < minspeed:

      # See rules 6.3 and 6.4.

      self._log("- speed is below the minimum of %.1f." % minspeed)
      self._log("- aircraft is stalled.")
      if flighttype != "ST":
        raise RuntimeError("flight type must be ST.")

    elif flighttype == "ST":

      raise RuntimeError("flight type cannot be ST as aircraft is not stalled.")

    elif lastflighttype == "ST":

      # See rule 6.4.

      if _isclimbing(flighttype):
        raise RuntimeError("flight type immediately after ST must not be climbing.")

  
  ##############################################################################

  def startmove(self, flighttype, power, actions, flamedoutfraction=0):

    """
    Start a move, declaring the flight type and power, and possible carrying 
    out some actions.
    """

    aplog.clearerror()
    try:

     self._log("--- start of move --")

     self._restore(apturn.turn() - 1)

     if self._destroyed or self._leftmap:
       self._endmove()
       return

     # We save values of these variables at the end of the previous move.

     self._lastconfiguration = self._configuration
     self._lastpowersetting  = self._powersetting
     self._lastflighttype    = self._flighttype
     self._lastaltitudeband  = self._altitudeband
     self._lastspeed         = self._speed

     # These account for the APs associated with power, speed, speed-brakes, 
     # turns (split into the part for the maximum turn rate and the part for 
     # sustained turns), and altitude loss or gain.

     self._powerap         = 0
     self._speedap         = 0
     self._spbrap          = 0
     self._turnrateap      = 0
     self._sustainedturnap = 0
     self._altitudeap      = 0

     # The maximum turn rate in the current move. 
    
     self._maxturnrate      = None

     self._flighttype       = flighttype
     self._checkflighttype()

     self._speed,           \
     self._powersetting,    \
     self._powerap,         \
     self._speedap          = self._startmovespeed(power, flamedoutfraction)
  
     if self._turnfp > 0:
       turncarry = "%d %s%s" % (self._turnfp, self._bank, self._turnrate)
     else:
       turncarry = "0"
     self._log("carrying %+.2f APs, %s altitude levels, and %s turn FPs." % (
       self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry), turncarry
     ))
      
     if self._flighttype == "ST":

       self._fpcarry = 0
       self._turnsstalled += 1
       self._dostalledflight(actions)
       self._endmove()

     elif self._flighttype == "DP":

       self._fpcarry = 0
       self._turnsdeparted += 1
       self._dodepartedflight(actions)
       self._endmove()
        
     else:

       self._turnsstalled  = 0
       self._turnsdeparted = 0
       self._startnormalflight(actions)

    except RuntimeError as e:
      aplog.logerror(e)

  ################################################################################

  def continuemove(self, actions):

    """
    Continue a move that has been started, possible carrying out some actions.
    """

    aplog.clearerror()
    try:

      if self._destroyed or self._leftmap or self._flighttype == "ST" or self._flighttype == "DP":
        return

      self._continuenormalflight(actions)

    except RuntimeError as e:
      aplog.logerror(e)

  ################################################################################

  def _endmove(self):

    """
    Process the end of a move.
    """

    self._drawaircraft("end")
    self._log("---")
    
    if self._destroyed:
    
      self._log("aircraft has been destroyed.")

    elif self._leftmap:

      self._log("aircraft has left the map.")

    else:

      if self._flighttype != "ST" and self._flighttype != "DP":
        self._log("used %d HFPs and %d VFPs (and %.1f FPs to speedbrakes)." % (self._hfp, self._vfp, self._spbrfp))

      if self._lastconfiguration != self._configuration:
        self._log("configuration changed from %s to %s." % (self._lastconfiguration, self._configuration))
      else:
        self._log("configuration is unchanged at %s." % self._configuration)
              
      if self._lastaltitudeband != self._altitudeband:
        self._log("altitude band changed from %s to %s." % (self._lastaltitudeband, self._altitudeband))
      else:
        self._log("altitude band is unchanged at %s." % self._altitudeband)
        
      if self._maxturnrate != None:
        self._log("maximum turn rate was %s." % self._maxturnrate)
        
      self._endmovespeed()

      if self._turnfp > 0:
        turncarry = "%d %s%s" % (self._turnfp, self._bank, self._turnrate)
      else:
        turncarry = "0"
      self._log("carrying %.1f FPs, %+.2f APs, %s altitude levels, and %s turn FPs." % (
        self._fpcarry, self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry), turncarry
      ))

    self._save(apturn.turn())

    self._log("--- end of move -- ")
    self._logbreak()

################################################################################
