"""OSC handler for TouchDesigner — parses incoming puck data and updates shared storage.

HOW TO USE IN TD:
  1. Add an OSC In CHOP, set port=7000, protocol=UDP
  2. Add a Script CHOP, set language=Python
  3. In the Script CHOP's 'onCook' script: exec(open('touchdesigner/scripts/osc_handler.py').read())
     OR reference this file via Script DAT → Execute Script

  Alternatively: use a CHOP Execute DAT watching the OSC In CHOP.
  See VERTICAL-SLICE-RUNBOOK.md for the exact node graph.

DATA CONTRACT (matches vision/src/osc_send.py):
  /puck/detected   id(int) frame(int) proj_x(float) proj_y(float) in_target(int)
  /puck/lost       id(int)
  /vision/heartbeat  frame(int)

STORAGE (op('storage') or parent().store / fetch):
  pucks[id] = {
      'projector_xy': (px, py),
      'in_target': bool,
      'last_frame': int,
      'lost': False
  }
  vision_alive: bool  — True if heartbeat received within HEARTBEAT_TIMEOUT_SEC
  last_heartbeat_frame: int
"""

# This module is designed to be pasted into a TD Script DAT or called from one.
# All TD-specific APIs (op, me, storage) are available in that context.

HEARTBEAT_TIMEOUT_FRAMES = 60  # ~2s at 30fps — mark pipeline dead if no heartbeat


def onReceiveOSC(dat, rowIndex, message, bytes, timeStamp, address, args, peer):
    """Called by TD's OSC In DAT for each incoming message.

    Attach this DAT's script to an OSC In DAT using a DAT Execute.
    """
    store = op('storage')  # Text DAT used as a JSON store, or use parent().store/fetch

    if address == '/puck/detected':
        pid, frame, px, py, in_target = int(args[0]), int(args[1]), float(args[2]), float(args[3]), int(args[4])
        _update_puck(pid, frame, px, py, bool(in_target))

    elif address == '/puck/lost':
        pid = int(args[0])
        _mark_puck_lost(pid)

    elif address == '/vision/heartbeat':
        parent().store('vision_alive', True)
        parent().store('last_heartbeat_frame', int(args[0]))


def _update_puck(pid: int, frame: int, px: float, py: float, in_target: bool):
    pucks = parent().fetch('pucks', {})
    pucks[pid] = {
        'projector_xy': (px, py),
        'in_target': in_target,
        'last_frame': frame,
        'lost': False,
    }
    parent().store('pucks', pucks)


def _mark_puck_lost(pid: int):
    pucks = parent().fetch('pucks', {})
    if pid in pucks:
        pucks[pid]['lost'] = True
    parent().store('pucks', pucks)


def check_heartbeat_timeout(current_frame: int):
    """Call from a Timer CHOP execute or per-cook script to detect pipeline death."""
    last = parent().fetch('last_heartbeat_frame', -9999)
    alive = (current_frame - last) < HEARTBEAT_TIMEOUT_FRAMES
    parent().store('vision_alive', alive)
    return alive
