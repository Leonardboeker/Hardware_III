"""Final push - load Slider B code directly into DATs from the WORKTREE,
strip BOM, disable file-sync, and force re-evaluation.
"""

import pathlib

# Source of truth: the worktree where Slider B actually lives
SRC = pathlib.Path('D:/IAAC/Hardware_III/.claude/worktrees/objective-leakey-a3a366/touchdesigner/scripts')

loads = {
    'compute_state_callbacks':    SRC / 'vision2_state_chop.py',
    'vision2_state_callbacks':    SRC / 'vision2_state_chop.py',
    'render_footprint_callbacks': SRC / 'footprint_viz_v5.py',
    'serial1_callbacks':          SRC / 'serial_rfid_v1.py',
    'rfid_serial_callbacks':      SRC / 'serial_rfid_v1.py',
    'panel_text':                 SRC / 'panel_text.py',
}

print('=' * 60)
print('Force-load (worktree -> DAT, strip BOM, disable sync)')
print('=' * 60)

for dat_name, src_path in loads.items():
    dat = op('/project1/' + dat_name)
    if dat is None:
        print('  SKIP ' + dat_name + '  (DAT missing)')
        continue
    if not src_path.exists():
        print('  FAIL ' + dat_name + '  (source missing: ' + str(src_path) + ')')
        continue

    # Read file as bytes, strip UTF-8 BOM (EF BB BF), decode
    raw_bytes = src_path.read_bytes()
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        raw_bytes = raw_bytes[3:]
        print('  (stripped BOM from ' + src_path.name + ')')
    text = raw_bytes.decode('utf-8')

    # Disable file-sync FIRST so writing dat.text does not push to disk
    if hasattr(dat.par, 'syncfile'):
        try:
            dat.par.syncfile = False
        except Exception:
            pass

    old_len = len(dat.text)
    dat.text = text
    new_len = len(dat.text)
    print('  OK ' + dat_name.ljust(30) + '  ' + str(old_len) + ' -> ' + str(new_len) + ' bytes')

    # Force module re-evaluation
    if hasattr(dat.par, 'module'):
        try:
            cur = dat.par.module.eval()
            dat.par.module = False
            dat.par.module = bool(cur) if cur is not None else True
        except Exception:
            pass

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

print('')
print('=' * 60)
print('Verify compute_state channels')
print('=' * 60)
cs = op('/project1/compute_state')
if cs is not None:
    chans = [c.name for c in cs.chans('*')]
    print('compute_state has ' + str(len(chans)) + ' channels:')
    needed = ['floor', 'slider_raw', 'slider_alive',
              'phase_slider_raw', 'phase_index', 'phase_slider_alive', 'wrapper_state']
    for c in chans:
        marker = '  *' if c in needed else '   '
        try:
            v = cs[c][0]
            print(marker + c.ljust(22) + ' = ' + str(v))
        except Exception:
            print(marker + c.ljust(22))

    missing = [n for n in needed if n not in chans]
    if missing:
        print('STILL MISSING: ' + str(missing))
    else:
        print('ALL 7 SLIDER CHANNELS PRESENT')
