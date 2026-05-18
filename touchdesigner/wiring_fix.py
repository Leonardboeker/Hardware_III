"""TD wiring fix - repoints all File-Sync paths + auto-runs Onur's bootstrap.

Run from TouchDesigner textport (Alt+T):

    exec(open('D:/IAAC/Hardware_III/touchdesigner/wiring_fix.py').read())

Uses direct op('/project1/<name>') access (findChildren had a quirk).
Uses absolute D:/IAAC/Hardware_III paths because the .toe was opened from
the repo root.

After path fix, automatically calls bootstrap_metric_ui.bootstrap_metric_ui(owner=root)
per Onur's LEO-TD-INTEGRATION-GUIDE.md.
"""

REPO = 'D:/IAAC/Hardware_III'

mappings = {
    'panel_text':                 REPO + '/touchdesigner/scripts/panel_text.py',
    'methods_db':                 REPO + '/data/methods_db.json',
    'script2_callbacks':          REPO + '/touchdesigner/scripts/state_chop_v1.py',
    'metrics_engine':             REPO + '/touchdesigner/scripts/metrics_engine.py',
    'bootstrap_metric_ui':        REPO + '/touchdesigner/scripts/metric_ui_bootstrap.py',
    'ui_state':                   REPO + '/touchdesigner/scripts/ui_state.py',
    'lca_data':                   REPO + '/touchdesigner/scripts/lca_data_reader.py',
    'lca_data_callbacks':         REPO + '/touchdesigner/scripts/lca_data_reader.py',
    'rfid_serial_callbacks':      REPO + '/touchdesigner/scripts/serial_rfid_v1.py',
    'serial1_callbacks':          REPO + '/touchdesigner/scripts/serial_rfid_v1.py',
    'compute_state_callbacks':    REPO + '/touchdesigner/scripts/vision2_state_chop.py',
    'vision2_state_callbacks':    REPO + '/touchdesigner/scripts/vision2_state_chop.py',
    'render_footprint_callbacks': REPO + '/touchdesigner/scripts/footprint_viz_v5.py',
    'refresh_metrics_ui':         REPO + '/touchdesigner/scripts/metric_ui_bootstrap.py',
    'method_preview_masonry':     REPO + '/touchdesigner/assets/method_loops/masonry_mode.gif',
    'method_preview_3d_printed':  REPO + '/touchdesigner/assets/method_loops/3d_printed_mode.gif',
    'method_preview_prefab':      REPO + '/touchdesigner/assets/method_loops/prefab_mode.gif',
}

print('=' * 60)
print('[wiring-fix] Phase 1: file paths')
print('=' * 60)

fixed = 0
missing = []
for name, path in mappings.items():
    node = op('/project1/' + name)
    if node is None:
        missing.append(name)
        continue
    if hasattr(node.par, 'file'):
        node.par.file = path
        if hasattr(node.par, 'syncfile'):
            node.par.syncfile = True
        # Force reload from file
        if hasattr(node.par, 'loadonstart'):
            node.par.loadonstart = True
        fixed += 1
        print('  OK ' + node.path + '  ->  ' + path)
    else:
        print('  WARN ' + name + ' has no .file parameter')

print('[wiring-fix] updated ' + str(fixed) + ' node(s)')
if missing:
    print('[wiring-fix] not found in /project1: ' + str(missing))

print('')
print('=' * 60)
print('[wiring-fix] Phase 2: reload DATs from file')
print('=' * 60)

# Force reload each DAT to pick up the new file content
reloaded = 0
for name in mappings.keys():
    node = op('/project1/' + name)
    if node is None:
        continue
    # Pulse the reload button if it exists
    if hasattr(node.par, 'loadonstartpulse'):
        try:
            node.par.loadonstartpulse.pulse()
            reloaded += 1
        except Exception as e:
            pass
print('[wiring-fix] reloaded ' + str(reloaded) + ' DAT(s)')

print('')
print('=' * 60)
print('[wiring-fix] Phase 3: Onur bootstrap (rebuilds runtime DATs)')
print('=' * 60)

try:
    root = op('/project1')
    boot_dat = op('/project1/bootstrap_metric_ui')
    if boot_dat is None:
        print('  SKIP - bootstrap_metric_ui not found in /project1')
    else:
        # Make sure the DAT is treated as a module
        try:
            boot_dat.par.module = True
        except Exception:
            pass
        boot = boot_dat.module
        boot.bootstrap_metric_ui(owner=root)
        print('  OK bootstrap_metric_ui(owner=root) ran')

        refresh_dat = op('/project1/refresh_metrics_ui')
        if refresh_dat is not None:
            refresh_dat.module.refresh(owner=root)
            print('  OK refresh_metrics_ui.refresh(owner=root) ran')

        render = op('/project1/render_footprint')
        if render is not None:
            render.cook(force=True)
            print('  OK render_footprint cooked')
except Exception as exc:
    print('  ERROR bootstrap failed: ' + str(exc))
    import traceback
    traceback.print_exc()

print('')
print('[wiring-fix] DONE.  Save the .toe (Ctrl+S) to persist these path changes.')
