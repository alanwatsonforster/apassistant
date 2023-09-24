import airpower.altitude as apaltitude
import airpower.azimuth  as apazimuth
import airpower.draw     as apdraw
import airpower.hex      as aphex
import airpower.hexcode  as aphexcode
import airpower.map      as apmap

import math

class Aircraft:

  def __init__(self, name, hexcode, azimuth, altitude, speed):

    x, y = aphexcode.toxy(hexcode)
    facing = apazimuth.tofacing(azimuth)

    apaltitude.checkisvalidaltitude(altitude)
    aphex.checkisvalidfacing(x, y, facing)

    self._turn          = 0
    self._name          = name

    self._x             = x
    self._y             = y
    self._facing        = facing
    self._altitude      = altitude
    self._altitudecarry = 0
    self._speed         = speed
    self._fpcarry       = 0
    self._apcarry       = 0

    self._destroyed     = False
    self._leftmap       = False

    self._saved = []
    self._save(0)

    self._drawaircraft("end")

  def __str__(self):
    return "[name: %s]" % self._name

   ##############################################################################

  # Drawing

  def _drawflightpath(self, lastx, lasty):
    apdraw.drawflightpath(lastx, lasty, self._x, self._y)

  def _drawaircraft(self, when):
    apdraw.drawaircraft(self._x, self._y, self._facing, self._name, self._altitude, when)
        
   ##############################################################################

  # Reporting

  def _formatposition(self):
    if apmap.isonmap(self._x, self._y):
      sheet = apmap.tosheet(self._x, self._y)
      hexcode = aphexcode.fromxy(self._x, self._y)
    else:
      sheet = "--"
      hexcode = "----"
    azimuth = apazimuth.fromfacing(self._facing)
    altitude = self._altitude
    return "%2s %-9s  %-3s  %2d" % (sheet, hexcode, azimuth, altitude)

  def _formatifp(self):
    if self._turn == 0:
      return ""
    else:
      return "FP %d" % (self._hfp + self._vfp)

  def _report(self, s):
    print("%s: turn %-2d : %s" % (self._name, self._turn, s))

  def _reportbreak(self):
    print()

  def _reportposition(self):
    self._report("%-5s : %-16s : %s" % ("", "", self._formatposition()))

  def _reportactionsandposition(self, action):
    self._report("%-5s : %-16s : %s" % (self._formatifp(), action, self._formatposition()))
  
  def _reportevent(self, s):
    self._report("%-5s : %s" % (self._formatifp(), s))

  def _reportstartofturn(self):

    self._report("--- start of turn -- ")

    if self._destroyed:
      self._report("aircraft has been destroyed.")
      return

    if self._leftmap:
      self._report("aircraft has left the map.")
      return

    self._report("speed is %.1f." % (self._speed, self._m1()))
    self._report("%.1f FPs available." % self._nfp)
    self._report("--- ")

    self._reportactionsandposition("")

  def _reportendofturn(self):

    if not self._destroyed and not self._leftmap:

      self._report("--- ")

      self._report("%d HFPs, %d VFPs, %.1f SFPs, and %+.1f APs." % (self._hfp, self._vfp, self._sfp, self._ap))

      initialspeed = self._speed
      if self._ap <= 0:
        aprate = -2.0
      elif initialspeed >= self._m1():
        aprate = +3.0
      else:
        aprate = +2.0
      if self._ap >= 0:
        self._speed += 0.5 * (self._ap // aprate)
        self._apcarry = self._ap % aprate
      else:
        self._speed -= 0.5 * (self._ap // aprate)
        self._apcarry = self._ap % aprate

      if self._speed != initialspeed:
        self._report("speed changed from %.1f to %.1f." % (initialspeed, self._speed))
      else:
        self._report("speed is unchanged at %.1f." % self._speed)

      initialaltitudeband = self._altitudeband
      self._altitudeband = apaltitude.altitudeband(self._altitude)
      if self._altitudeband != initialaltitudeband:
        self._report("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
      else:
        self._report("altitude band is unchanged at %s." % self._altitudeband)

      self._report("carrying %.1f FPs, %+.1f APs, and %s altitude levels." % (
        self._fpcarry, self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
      ))

    self._report("--- end of turn -- ")
    self._reportbreak()

  #############################################################################

  # Elements

  def _A(self, what):
    self._reportevent("attack with %s." % what)

  def _C(self, altitudechange):
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, +altitudechange)

  def _D(self, altitudechange):
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)

  def _H(self):
    self._x, self._y = aphex.nextposition(self._x, self._y, self._facing)

  def _K(self):
    self._reportevent("aircraft has been killed.")
    self._destroyed = True

  def _L(self, facingchange):
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoleft(self._x, self._y, self._facing)
    self._facing = (self._facing + facingchange) % 360

  def _R(self, facingchange):
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoright(self._x, self._y, self._facing)
    self._facing = (self._facing - facingchange) % 360

  def _S(self, sfp):
    if self._sfp != 0:
      raise ValueError("speedbrakes can only be used once per turn.")
    maxsfp = self._nfp - self._hfp - self._vfp
    if sfp > maxsfp:
      raise ValueError("attempt to use speedbrakes to eliminate %s FPs but only %s are remaining." % (sfp, maxsfp))
    self._sfp = sfp

  def _getelementdispatchlist(self):
  
    return [

      # This table is searched in order, so put longer elements before shorter 
      # ones that are prefixes (e.g., put C2 before C and D3/4 before D3).

      # [0] is the element code.
      # [1] is the procedure for movement elements.
      # [2] is the procedure for other (non-movement) elements.

      ["H"   , lambda : self._H()   , lambda : None],

      ["C1/8", lambda : self._C(1/8), lambda: None],
      ["C1/4", lambda : self._C(1/4), lambda: None],
      ["C3/8", lambda : self._C(3/8), lambda: None],
      ["C1/2", lambda : self._C(1/2), lambda: None],
      ["C5/8", lambda : self._C(5/8), lambda: None],
      ["C3/4", lambda : self._C(3/4), lambda: None],
      ["C7/8", lambda : self._C(7/8), lambda: None],
      ["C⅛"  , lambda : self._C(1/8), lambda: None],
      ["C¼"  , lambda : self._C(1/4), lambda: None],
      ["C⅜"  , lambda : self._C(3/8), lambda: None],
      ["C½"  , lambda : self._C(1/2), lambda: None],
      ["C⅝"  , lambda : self._C(5/8), lambda: None],
      ["C¾"  , lambda : self._C(3/4), lambda: None],
      ["C⅞"  , lambda : self._C(7/8), lambda: None],
      ["C1"  , lambda : self._C(1)  , lambda: None],
      ["C2"  , lambda : self._C(2)  , lambda: None],
      ["CC"  , lambda : self._C(2)  , lambda: None],
      ["C"   , lambda : self._C(1)  , lambda: None],

      ["D1/8", lambda : self._D(1/8), lambda: None],
      ["D1/4", lambda : self._D(1/4), lambda: None],
      ["D3/8", lambda : self._D(3/8), lambda: None],
      ["D1/2", lambda : self._D(1/2), lambda: None],
      ["D5/8", lambda : self._D(5/8), lambda: None],
      ["D3/4", lambda : self._D(3/4), lambda: None],
      ["D7/8", lambda : self._D(7/8), lambda: None],
      ["D⅛"  , lambda : self._D(1/8), lambda: None],
      ["D¼"  , lambda : self._D(1/4), lambda: None],
      ["D⅜"  , lambda : self._D(3/8), lambda: None],
      ["D½"  , lambda : self._D(1/2), lambda: None],
      ["D⅝"  , lambda : self._D(5/8), lambda: None],
      ["D¾"  , lambda : self._D(3/4), lambda: None],
      ["D⅞"  , lambda : self._D(7/8), lambda: None],
      ["D1"  , lambda : self._D(1)  , lambda: None],
      ["D2"  , lambda : self._D(2)  , lambda: None],
      ["D3"  , lambda : self._D(3)  , lambda: None],
      ["DDD" , lambda : self._D(3)  , lambda: None],
      ["DD"  , lambda : self._D(2)  , lambda: None],
      ["D"   , lambda : self._D(1)  , lambda: None],

      ["L90" , lambda : self._L(90) , lambda: None],
      ["L60" , lambda : self._L(60) , lambda: None],
      ["L30" , lambda : self._L(30) , lambda: None],
      ["LLL" , lambda : self._L(90) , lambda: None],
      ["LL"  , lambda : self._L(60) , lambda: None],
      ["L"   , lambda : self._L(30) , lambda: None],

      ["R90" , lambda : self._R(90) , lambda: None],
      ["R60" , lambda : self._R(60) , lambda: None],
      ["R30" , lambda : self._R(30) , lambda: None],
      ["RRR" , lambda : self._R(90) , lambda: None],
      ["RR"  , lambda : self._R(60) , lambda: None],
      ["R"   , lambda : self._R(30) , lambda: None],

      ["S1/2", lambda: self._S(1/2) , lambda: None],
      ["S3/2", lambda: self._S(3/2) , lambda: None],
      ["S½"  , lambda: self._S(1/2) , lambda: None],
      ["S1½" , lambda: self._S(3/2) , lambda: None],
      ["S1"  , lambda: self._S(1)   , lambda: None],
      ["S2"  , lambda: self._S(2)   , lambda: None],
      ["SSSS", lambda: self._S(2)   , lambda: None],
      ["SSS" , lambda: self._S(3/2) , lambda: None],
      ["SS"  , lambda: self._S(1)   , lambda: None],
      ["S"   , lambda: self._S(1/2) , lambda: None],

      ["/"   , lambda : None        , lambda: None],

      ["AGN" , lambda : None        , lambda: self._A("guns")],
      ["AGP" , lambda : None        , lambda: self._A("gun pod")],
      ["ARK" , lambda : None        , lambda: self._A("rockets")],
      ["ARP" , lambda : None        , lambda: self._A("rocket pods")],

      ["K"   , lambda : None        , lambda: self._K()],

    ]

  ##############################################################################

  def checkforterraincollision(self):
    altitudeofterrain = apaltitude.terrainaltitude()
    if self._altitude <= altitudeofterrain:
      self._altitude = altitudeofterrain
      self._altitudecarry = 0
      self._reportevent("aircraft has collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True

  def checkforleavingmap(self):
    if not apmap.iswithinmap(self._x, self._y):
      self._reportevent("aircraft has left the map.")
      self._leftmap = True
  
  ##############################################################################

  # Turn management
  
  def _restore(self, i):
    self._x, \
    self._y, \
    self._facing, \
    self._altitude, \
    self._altitudecarry, \
    self._speed, \
    self._fpcarry, \
    self._apcarry, \
    self._destroyed, \
    self._leftmap \
    = self._saved[i]

  def _save(self, i):
    if len(self._saved) == i:
      self._saved.append(None)
    self._saved[i] = ( \
      self._x, \
      self._y, \
      self._facing, \
      self._altitude, \
      self._altitudecarry, \
      self._speed, \
      self._fpcarry, \
      self._apcarry, \
      self._destroyed, \
      self._leftmap, \
    )

  def _maxprevturn(self):
    return len(self._saved) - 1

  def start(self, turn, ap, actions):

    if turn > self._maxprevturn() + 1:
      raise ValueError("turn %d is out of sequence." % turn)

    self._restore(turn - 1)

    self._turn         = turn
    self._hfp          = 0
    self._vfp          = 0
    self._sfp          = 0
    self._nfp          = self._speed + self._fpcarry
    self._altitudeband = apaltitude.altitudeband(self._altitude)
    self._ap           = ap + self._apcarry

    self._reportstartofturn()

    if self._destroyed or self._leftmap:
        self._reportendofturn()
        self._save(self._turn)
        return
 
    if actions != "":
      self.next(actions)

  def next(self, actions):

    if self._destroyed or self._leftmap:
      return

    for action in actions.split(","):

      if self._hfp + self._vfp + self._sfp + 1 > self._nfp:
        raise ValueError("only %d FPs are available." % self._nfp)
    
      if action[0] == 'H':
        self._hfp += 1
      elif action[0] == 'D' or action[0] == 'C':
        self._vfp += 1
      else:
        raise ValueError("action %s does not begin with H, D, or C." % action)

      lastx = self._x
      lasty = self._y

      elementdispatchlist = self._getelementdispatchlist()

      # Execute movement elements.
      a = action
      while a != "":
        for element in elementdispatchlist:
          if element[0] == a[:len(element[0])]:
            element[1]()
            a = a[len(element[0]):]
            break
        else:
          raise ValueError("unknown element %s in action %s." % (a, action))

      self._reportactionsandposition(action)
      self._drawflightpath(lastx, lasty)

      self.checkforterraincollision()
      self.checkforleavingmap()
      if self._destroyed or self._leftmap:
        break

      # Execute other elements.
      a = action
      while a != "":
        for element in elementdispatchlist:
          if element[0] == a[:len(element[0])]:
            element[2]()
            a = a[len(element[0]):]
            break
        else:
          raise ValueError("unknown element %s in action %s." % (a, action))

      if self._destroyed:
        break

    assert self._hfp + self._vfp + self._sfp <= self._nfp
    assert aphex.isvalidposition(self._x, self._y)
    assert aphex.isvalidfacing(self._x, self._y, self._facing)
    assert apaltitude.isvalidaltitude(self._altitude)

    if self._hfp + self._vfp + self._sfp + 1 > self._nfp or self._destroyed or self._leftmap:

      self._fpcarry = self._nfp - self._hfp - self._vfp - self._sfp

      self._reportendofturn()
      self._drawaircraft("end")
      self._save(self._turn)
      
    else:
      
      self._drawaircraft("next")
