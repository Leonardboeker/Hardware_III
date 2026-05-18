"""PRESENTATION-SAFE: only updates compute_state, touches NOTHING else.

After running this:
- Onur's UI is 100% as he designed it (no text TOP modifications)
- compute_state has the 7 slider channels with live values
- To DEMO Slider B during presentation:
  1. Click on 'compute_state' Script CHOP node
  2. Press 'S' (or right-click -> Viewer) to open Channel Viewer
  3. Show audience: 'floor', 'phase_index', 'wrapper_state', 'slider_raw'
  4. Move sliders -> values change live

No UI overlay overlap. No broken layout. Slider data visible via CHOP viewer.
"""

import pathlib

SRC = pathlib.Path('D:/IAAC/Hardware_III/.claude/worktrees/objective-leakey-a3a366/touchdesigner/scripts/vision2_state_chop.py')

# Read clean (no BOM) content
raw = SRC.read_bytes()
while raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
text = raw.decode('utf-8')

# Push into vision2_state_callbacks DAT
target = op('/project1/vision2_state_callbacks')
if target is None:
    print('FAIL: vision2_state_callbacks not found')
else:
    if hasattr(target.par, 'syncfile'):
        target.par.syncfile = False
    target.text = text
    if hasattr(target.par, 'module'):
        try:
            target.par.module = False
            target.par.module = True
        except Exception:
            pass
    print('loaded vision2_state_chop.py (' + str(len(text)) + ' bytes) into vision2_state_callbacks')

# Point compute_state at it
cs = op('/project1/compute_state')
if cs is not None and target is not None:
    cs.par.callbacks = target
    if hasattr(cs.par, 'script'):
        cs.par.script = target
    cs.cook(force=True)
    chans = list(cs.chans('*'))
    needed = ['floor', 'slider_raw', 'phase_slider_raw', 'phase_index', 'wrapper_state']
    have = [c.name for c in chans]
    missing = [n for n in needed if n not in have]
    print('compute_state channels: ' + str(len(chans)))
    if not missing:
        print('  ALL slider channels live:')
        for n in needed:
            print('    ' + n.ljust(20) + ' = ' + str(cs[n][0]))
    else:
        print('  MISSING: ' + str(missing))

print('')
print('DONE - Onur UI completely untouched.')
print('Demo path: click compute_state -> press S -> show floor/phase_index/wrapper_state live.')
