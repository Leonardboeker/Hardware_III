"""Re-push vision2_state_chop.py into compute_state_callbacks + force cook.
Defensive: checks each channel before accessing.
"""

import pathlib

SRC = pathlib.Path('D:/IAAC/Hardware_III/.claude/worktrees/objective-leakey-a3a366/touchdesigner/scripts/vision2_state_chop.py')

# Re-push fresh content
raw = SRC.read_bytes()
if raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
text = raw.decode('utf-8')

dat = op('/project1/compute_state_callbacks')
if dat is None:
    print('FAIL: compute_state_callbacks not found')
else:
    if hasattr(dat.par, 'syncfile'):
        dat.par.syncfile = False
    dat.text = text
    if hasattr(dat.par, 'module'):
        try:
            dat.par.module = False
            dat.par.module = True
        except Exception:
            pass
    print('pushed ' + str(len(text)) + ' bytes into compute_state_callbacks')

cs = op('/project1/compute_state')
if cs is not None:
    cs.cook(force=True)

# Defensive channel read
print('')
print('=' * 50)
print('compute_state channels:')
print('=' * 50)
if cs is None:
    print('FAIL: compute_state not found')
else:
    chans = list(cs.chans('*'))
    print('total: ' + str(len(chans)))
    for c in chans:
        try:
            v = c[0]
        except Exception:
            v = '?'
        marker = '  *' if c.name in ('floor', 'slider_raw', 'slider_alive', 'phase_slider_raw', 'phase_index', 'phase_slider_alive', 'wrapper_state') else '   '
        print(marker + c.name.ljust(22) + ' = ' + str(v))

# Also probe rfid_in storage directly (independent of compute_state)
print('')
print('=' * 50)
print('rfid_in storage (independent check):')
print('=' * 50)
rfid = op('/project1/rfid_in')
if rfid is not None:
    for key in ['method_id', 'floor', 'slider_raw', 'slider_last_frame',
                'phase_slider_raw', 'phase_slider_last_frame']:
        v = rfid.fetch(key, '<not stored>')
        print('  ' + key.ljust(25) + ' = ' + str(v))
