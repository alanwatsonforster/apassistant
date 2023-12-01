"""
Logging.
"""


import apxo.turn as apturn

_silent = False

def log(s):
  if _silent:
    return
  if apturn.turn() is None:
    print(s)
  elif apturn.turn() == 0:
    print("set-up: %s" % s)
  else:
    print("turn %d: %s" % (apturn.turn(), s))

def logbreak():
  if _silent:
    return
  print()

_error = None

def clearerror():
  global _error
  _error = None

def logexception(e):
  global _error
  _error = str(e.args[0])
  if _silent:
    return
  logbreak()
  log("=== ERROR: %s ===" % _error)
  logbreak()

def plural(i, singular, plural):
  if i == 1:
    return singular
  else:
    return plural