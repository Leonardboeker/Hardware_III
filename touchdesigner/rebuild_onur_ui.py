"""Rebuild Onur's UI via bootstrap_metric_ui, with metrics_engine bypassed.

Strategy:
1. Bypass metrics_engine + ui_state + refresh_metrics_ui first (they error
   because Onur's CSV pipeline schema mismatch — not our concern)
2. Run bootstrap which rebuilds all text TOPs with proper expressions
3. Re-apply Slider B integration (compute_state + text_bar_bottom_status)
"""

print('=' * 60)
print('Step 1: Bypass broken Onur metrics pieces')
print('=' * 60)
for name in ['metrics_engine', 'ui_state', 'refresh_metrics_ui']:
    n = op('/project1/' + name)
    if n is None:
        continue
    # Set the DAT to bypass = don't execute its module callbacks
    try:
        if hasattr(n.par, 'bypass'):
            n.par.bypass = True
            print('  bypass=ON  ' + name)
    except Exception as e:
        print('  could not bypass ' + name + ': ' + str(e))

print('')
print('=' * 60)
print('Step 2: Run Onur bootstrap to rebuild text TOPs')
print('=' * 60)
try:
    root = op('/project1')
    boot_dat = op('/project1/bootstrap_metric_ui')
    if boot_dat is None:
        print('FAIL: bootstrap_metric_ui not found')
    else:
        boot = boot_dat.module
        boot.bootstrap_metric_ui(owner=root)
        print('  bootstrap_metric_ui ran (text TOPs reconstructed)')
except Exception as e:
    print('  bootstrap had errors (expected for metrics part): ' + str(e))
    print('  text TOPs may have been partially reconstructed anyway')

print('')
print('=' * 60)
print('Step 3: Re-apply Slider B (compute_state -> vision2_state_callbacks)')
print('=' * 60)
import pathlib
SRC = pathlib.Path('D:/IAAC/Hardware_III/.claude/worktrees/objective-leakey-a3a366/touchdesigner/scripts/vision2_state_chop.py')
raw = SRC.read_bytes()
while raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
text = raw.decode('utf-8')

target = op('/project1/vision2_state_callbacks')
if target is not None:
    if hasattr(target.par, 'syncfile'):
        target.par.syncfile = False
    target.text = text
    if hasattr(target.par, 'module'):
        try:
            target.par.module = False
            target.par.module = True
        except Exception:
            pass

cs = op('/project1/compute_state')
if cs is not None and target is not None:
    cs.par.callbacks = target
    if hasattr(cs.par, 'script'):
        cs.par.script = target
    cs.cook(force=True)
    chans = list(cs.chans('*'))
    print('  compute_state channels: ' + str(len(chans)))

# Re-apply text_bar_bottom_status expression (bootstrap may have overwritten it)
tt = op('/project1/text_bar_bottom_status')
if tt is not None:
    try:
        tt.par.text.expr = "op('panel_text').module.bar_bottom_status()"
        tt.par.text.mode = ParMode.EXPRESSION
        tt.cook(force=True)
        print('  text_bar_bottom_status -> expression OK')
    except Exception as e:
        print('  text_bar_bottom_status FAIL: ' + str(e))

# Force cook render_footprint and projector
for n in ['render_footprint', 'projector_out']:
    op_n = op('/project1/' + n)
    if op_n is not None:
        try:
            op_n.cook(force=True)
        except Exception:
            pass

print('')
print('DONE — UI should look like Onurs setup but with metrics_engine bypassed (no error spam).')
