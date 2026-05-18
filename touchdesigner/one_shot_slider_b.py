"""One-shot Slider B integration after restoring pristine .toe.

Run from TouchDesigner textport ONCE after reopening the restored .toe:

    exec(open('D:/IAAC/Hardware_III/touchdesigner/one_shot_slider_b.py').read())

Steps:
1. Force-load vision2_state_chop.py into vision2_state_callbacks DAT
2. Force-load serial_rfid_v1.py into serial1_callbacks DAT
3. Force-load panel_text.py into panel_text DAT
4. Point compute_state.par.callbacks + script -> vision2_state_callbacks
5. Set ONLY text_bar_bottom_status as expression (don't touch other text TOPs)
6. Cook everything
7. Verify
"""

import pathlib

REPO = pathlib.Path('D:/IAAC/Hardware_III/.claude/worktrees/objective-leakey-a3a366')

def load_clean(src_rel):
    raw = (REPO / src_rel).read_bytes()
    while raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    return raw.decode('utf-8')

push_map = {
    'compute_state_callbacks': 'touchdesigner/scripts/vision2_state_chop.py',
    'vision2_state_callbacks': 'touchdesigner/scripts/vision2_state_chop.py',
    'serial1_callbacks':       'touchdesigner/scripts/serial_rfid_v1.py',
    'rfid_serial_callbacks':   'touchdesigner/scripts/serial_rfid_v1.py',
    'render_footprint_callbacks': 'touchdesigner/scripts/footprint_viz_v5.py',
    'panel_text':              'touchdesigner/scripts/panel_text.py',
}

print('--- 1. Force-load fresh code into DATs ---')
for dat_name, src_rel in push_map.items():
    dat = op('/project1/' + dat_name)
    if dat is None:
        continue
    if hasattr(dat.par, 'syncfile'):
        dat.par.syncfile = False
    dat.text = load_clean(src_rel)
    if hasattr(dat.par, 'module'):
        try:
            dat.par.module = False
            dat.par.module = True
        except Exception:
            pass
    print('  loaded ' + dat_name)

print('')
print('--- 2. Point compute_state at vision2_state_callbacks ---')
cs = op('/project1/compute_state')
target = op('/project1/vision2_state_callbacks')
if cs is not None and target is not None:
    cs.par.callbacks = target
    if hasattr(cs.par, 'script'):
        cs.par.script = target
    cs.cook(force=True)
    print('  compute_state channels: ' + str(len(list(cs.chans('*')))))

print('')
print('--- 3. Set text_bar_bottom_status as live expression (only one!) ---')
tt = op('/project1/text_bar_bottom_status')
if tt is not None:
    try:
        tt.par.text.expr = "op('panel_text').module.bar_bottom_status()"
        tt.par.text.mode = ParMode.EXPRESSION
        tt.cook(force=True)
        print('  text_bar_bottom_status -> expression OK')
    except Exception as e:
        print('  FAIL: ' + str(e))

print('')
print('--- 4. Verify ---')
if cs is not None:
    needed = ['floor', 'slider_raw', 'slider_alive',
              'phase_slider_raw', 'phase_index', 'phase_slider_alive', 'wrapper_state']
    chans = [c.name for c in cs.chans('*')]
    missing = [n for n in needed if n not in chans]
    if missing:
        print('  STILL MISSING: ' + str(missing))
    else:
        print('  ALL 7 SLIDER CHANNELS LIVE')
        for n in needed:
            try:
                print('    ' + n.ljust(22) + ' = ' + str(cs[n][0]))
            except Exception:
                pass

print('')
print('DONE. UI bottom bar should now show live FLOOR/PHASE.')
print('If happy, save (Ctrl+S) — sonst leave unsaved and re-run this script next session.')
