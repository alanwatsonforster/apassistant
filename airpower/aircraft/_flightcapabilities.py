import airpower.speed    as apspeed
import airpower.altitude as apaltitude

def power(self, powersetting):
  return self._aircraftdata.power(self._configuration, powersetting)

def spbr(self):
  return self._aircraftdata.spbr(self._configuration)

def fuelrate(self):
  return self._aircraftdata.fuelrate(self._powersetting)

def engines(self):
  return self._aircraftdata.engines()

def powerfade(self):
  return self._aircraftdata.powerfade(self._speed)

def turndrag(self, turnrate):
  if turnrate == "EZ":
    return 0.0
  lowspeedturnlimit = self._aircraftdata.lowspeedturnlimit()
  if lowspeedturnlimit == None:
    return self._aircraftdata.turndrag(self._configuration, turnrate)
  elif self._speed <= lowspeedturnlimit:
    return self._aircraftdata.turndrag(self._configuration, turnrate, lowspeed=True)
  else:
    return self._aircraftdata.turndrag(self._configuration, turnrate, highspeed=True)

def minspeed(self):
  minspeed = self._aircraftdata.minspeed(self._configuration, self._altitudeband)
  if minspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      minspeed = self._aircraftdata.minspeed(self._configuration, altitudeband)
      if minspeed != None:
        break
  return minspeed

def maxspeed(self):
  maxspeed = self._aircraftdata.maxspeed(self._configuration, self._altitudeband)
  if maxspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      maxspeed = self._aircraftdata.maxspeed(self._configuration, altitudeband)
      if maxspeed != None:
        break
  return maxspeed

def cruisespeed(self):
  return self._aircraftdata.cruisespeed()

def climbspeed(self):
  return self._aircraftdata.climbspeed()

def maxdivespeed(self):
  raw = self._aircraftdata.maxdivespeed(self._altitudeband)
  if raw != None:
    return raw
  # The aircraft is temporarily above its ceiling, so take the speed from the
  # highest band in the table.
  for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
    raw = self._aircraftdata.maxdivespeed(altitudeband)
    if raw != None:
      return raw

def ceiling(self):
  return self._aircraftdata.ceiling(self._configuration)

def rollhfp(self):
  return self._aircraftdata.rollhfp()

def rolldrag(self, rolltype):
  return self._aircraftdata.rolldrag(rolltype)

def climbcapability(self):
  climbcapability = self._aircraftdata.climbcapability(self._configuration, self._altitudeband, self._powersetting)
  if climbcapability == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      climbcapability = self._aircraftdata.climbcapability(self._configuration, altitudeband, self._powersetting)
      if climbcapability != None:
        break
  # See rule 6.6 and rule 8.1.4.
  if self._speed >= apspeed.m1speed(self._altitudeband):
    climbcapability *= 2/3
  return climbcapability

def hasproperty(self, p):
  if self._aircraftdata.hasproperty(p):
    return True
  if p == "HRR" and self._configuration == "CL":
    return self._aircraftdata.hasproperty("HRRCL")
  return False
