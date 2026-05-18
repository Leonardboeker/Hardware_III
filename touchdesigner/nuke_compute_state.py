"""Force TD to release ALL caches on compute_state's script source.

Tries multiple approaches:
1. Inspect current callbacks/script chain
2. Blank out callbacks + cook (should give 0 channels if callbacks were source)
3. Re-set callbacks to vision2_state_callbacks (different DAT, fresh)
4. Force module reload on the DAT
5. Cook with force
"""

import pathlib

cs = op('/project1/compute_state')
if cs is None:
    print('FAIL: compute_state not found')
else:
    print('=' * 60)
    print('Phase A: inspect current state')
    print('=' * 60)
    cb = cs.par.callbacks.eval() if hasattr(cs.par, 'callbacks') else None
    sc = cs.par.script.eval() if hasattr(cs.par, 'script') else None
    print('  par.callbacks -> ' + (cb.path if cb else 'None'))
    print('  par.script    -> ' + (sc.path if sc else 'None'))
    if cb:
        print('  callbacks DAT text length: ' + str(len(cb.text)))
        print('  callbacks DAT has "appendChan(\'wrapper_state\')": ' +
              str("'wrapper_state'" in cb.text or 'wrapper_state' in cb.text))

    print('')
    print('=' * 60)
    print('Phase B: clear callbacks + cook (test if callbacks were source)')
    print('=' * 60)
    cs.par.callbacks = ''
    if hasattr(cs.par, 'script'):
        cs.par.script = ''
    cs.cook(force=True)
    chans_empty = list(cs.chans('*'))
    print('  channels with empty callbacks/script: ' + str(len(chans_empty)))
    if chans_empty:
        print('  -> CHOP has INLINE script that overrides callbacks DAT')
        print('  -> Channel names: ' + str([c.name for c in chans_empty]))

    print('')
    print('=' * 60)
    print('Phase C: force fresh write into vision2_state_callbacks + use that')
    print('=' * 60)
    SRC = pathlib.Path('D:/IAAC/Hardware_III/.claude/worktrees/objective-leakey-a3a366/touchdesigner/scripts/vision2_state_chop.py')
    raw = SRC.read_bytes()
    while raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    text = raw.decode('utf-8')

    target = op('/project1/vision2_state_callbacks')
    if target is None:
        target = op('/project1/compute_state_callbacks')
    if hasattr(target.par, 'syncfile'):
        target.par.syncfile = False
    target.text = text
    if hasattr(target.par, 'module'):
        try:
            target.par.module = False
            target.par.module = True
        except Exception:
            pass

    # Set BOTH callbacks and script to target
    cs.par.callbacks = target
    if hasattr(cs.par, 'script'):
        cs.par.script = target

    cs.cook(force=True)
    chans_set = list(cs.chans('*'))
    print('  channels after callbacks=' + target.name + ': ' + str(len(chans_set)))

    print('')
    print('=' * 60)
    print('Phase D: result')
    print('=' * 60)
    chans = list(cs.chans('*'))
    print('compute_state has ' + str(len(chans)) + ' channels:')
    for c in chans:
        try:
            v = c[0]
        except Exception:
            v = '?'
        marker = '  *' if c.name in ('floor', 'slider_raw', 'phase_slider_raw', 'phase_index', 'wrapper_state', 'slider_alive', 'phase_slider_alive') else '   '
        print(marker + c.name.ljust(22) + ' = ' + str(v))
