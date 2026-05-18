"""V2 — force-load bootstrap_metric_ui.py into its DAT, then run bootstrap."""

import pathlib

REPO = pathlib.Path('D:/IAAC/Hardware_III/.claude/worktrees/objective-leakey-a3a366')

# 1. Force-load all relevant scripts into their DATs (clean, BOM-free)
loads = {
    'bootstrap_metric_ui':       REPO / 'touchdesigner/scripts/metric_ui_bootstrap.py',
    'metrics_engine':            REPO / 'touchdesigner/scripts/metrics_engine.py',
    'ui_state':                  REPO / 'touchdesigner/scripts/ui_state.py',
    'panel_text':                REPO / 'touchdesigner/scripts/panel_text.py',
    'refresh_metrics_ui':        REPO / 'touchdesigner/scripts/metric_ui_bootstrap.py',  # same file?
}

print('--- Force-load scripts ---')
for dat_name, src in loads.items():
    dat = op('/project1/' + dat_name)
    if dat is None:
        print('  SKIP ' + dat_name + ' (DAT missing)')
        continue
    if not src.exists():
        print('  SKIP ' + dat_name + ' (source missing)')
        continue
    raw = src.read_bytes()
    while raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    if hasattr(dat.par, 'syncfile'):
        dat.par.syncfile = False
    dat.text = raw.decode('utf-8')
    if hasattr(dat.par, 'module'):
        try:
            dat.par.module = False
            dat.par.module = True
        except Exception:
            pass
    print('  loaded ' + dat_name + ' (' + str(len(raw)) + ' bytes)')

# 2. Discover what functions bootstrap_metric_ui actually exports
print('')
print('--- bootstrap_metric_ui module attributes ---')
try:
    bm = op('/project1/bootstrap_metric_ui').module
    funcs = [a for a in dir(bm) if not a.startswith('_') and callable(getattr(bm, a, None))]
    print('  callable functions: ' + str(funcs))
except Exception as e:
    print('  ERROR introspect: ' + str(e))

# 3. Try common bootstrap function names
print('')
print('--- Try bootstrap ---')
root = op('/project1')
tried = ['bootstrap_metric_ui', 'bootstrap', 'rebuild', 'setup', 'init', 'main']
for fn in tried:
    try:
        bm = op('/project1/bootstrap_metric_ui').module
        f = getattr(bm, fn, None)
        if callable(f):
            try:
                f(owner=root)
                print('  OK called ' + fn + '(owner=root)')
                break
            except TypeError:
                # maybe no owner arg
                f()
                print('  OK called ' + fn + '()')
                break
    except Exception as e:
        print('  ' + fn + ' -> ' + str(e))

print('')
print('Done. Look at the UI now.')
