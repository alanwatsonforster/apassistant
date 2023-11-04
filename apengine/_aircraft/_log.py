"""
Logging for the aircraft class.
"""

import apengine      as ap
import apengine._log as aplog

def _log(self, s):
  aplog.log("%s: turn %-2d : %s" % (self._name, ap.turn(), s))

def _logbreak(self):
  aplog.logbreak()

def _logaction(self, s, t, u):
  self._log("%-5s : %-16s : %s" % (s, t, u))

def _logevent(self, s):
  self._log("%-5s : %s" % ("", s))

def _logstart(self, s):
  self._log("%-5s : %s" % ("start", s))

def _logend(self, s):
  self._log("%-5s : %s" % ("end", s))

def _logline(self):
  self._log("%-5s :" % "-----")  
