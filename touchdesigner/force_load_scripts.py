"""Force-write .py content directly into callback DATs and cook all consumers.

Bypasses TD's file-sync which silently failed to load my updated scripts.
"""

import pathlib

REPO = pathlib.Path('D:/IAAC/Hardware_III')

# Map DAT name -> .py file to load into it
loads = {
    'compute_state_callbacks':    REPO / 'touchdesigner/scripts/vision2_state_chop.py',
    'render_footprint_callbacks': REPO / 'touchdesigner/scripts/footprint_viz_v5.py',
    'serial1_callbacks':          REPO / 'touchdesigner/scripts/serial_rfid_v1.py',
    'rfid_serial_callbacks':      REPO / 'touchdesigner/scripts/serial_rfid_v1.py',
    'vision2_state_callbacks':    REPO / 'touchdesigner/scripts/vision2_state_chop.py',
    'panel_text':                 REPO / 'touchdesigner/scripts/panel_text.py',
}

print('=' * 60)
print('Force-load script content into DATs')
print('=' * 60)

for dat_name, src_path in loads.items():
    dat = op('/project1/' + dat_name)
    if dat is None:
        print('  SKIP ' + dat_name + '  (DAT not found)')
        continue
    if not src_path.exists():
        print('  FAIL ' + dat_name + '  (source missing: ' + str(src_path) + ')')
        continue
    new_text = src_path.read_text(encoding='utf-8')
    old_len = len(dat.text)
    dat.text = new_text
    print('  OK ' + dat_name + ' :  ' + str(old_len) + ' -> ' + str(len(new_text)) + ' bytes')

print('')
print('=' * 60)
print('Force-cook consumers')
print('=' * 60)

for name in ['compute_state', 'render_footprint']:
    n = op('/project1/' + name)
    if n is not None:
        try:
            n.cook(force=True)
            print('  OK cooked ' + name)
        except Exception as e:
            print('  FAIL cook ' + name + ': ' + str(e))
    else:
        print('  SKIP ' + name + ' (not found)')

print('')
print('=' * 60)
print('Verify compute_state channels')
print('=' * 60)
cs = op('/project1/compute_state')
if cs is not None:
    chans = [c.name for c in cs.chans('*')]
    print('compute_state has ' + str(len(chans)) + ' channels:')
    for c in chans:
        try:
            v = cs[c][0]
            print('  ' + c.ljust(22) + ' = ' + str(v))
        except Exception:
            print('  ' + c.ljust(22) + ' (no value)')
