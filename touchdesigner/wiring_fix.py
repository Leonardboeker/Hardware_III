"""TD wiring fix - repoints all File-Sync paths to D:/IAAC/Hardware_III absolute paths.

Run from TouchDesigner textport (Alt+T) with this single line:

    exec(open('D:/IAAC/Hardware_III/touchdesigner/wiring_fix.py').read())

Uses absolute paths because the .toe was opened from C:/Users/leona/Downloads/,
which made TD's project.folder unusable for relative path resolution.
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
    'method_preview_masonry':     REPO + '/touchdesigner/assets/method_loops/masonry_mode.gif',
    'method_preview_3d_printed':  REPO + '/touchdesigner/assets/method_loops/3d_printed_mode.gif',
    'method_preview_prefab':      REPO + '/touchdesigner/assets/method_loops/prefab_mode.gif',
}

fixed = 0
missing = []
for name, path in mappings.items():
    nodes = op('/project1').findChildren(name=name, depth=20)
    if not nodes:
        missing.append(name)
        continue
    for n in nodes:
        if hasattr(n.par, 'file'):
            n.par.file = path
            if hasattr(n.par, 'syncfile'):
                n.par.syncfile = True
            fixed += 1
            print('  -> ' + n.path + '  file = ' + path)

print('[wiring-fix] updated ' + str(fixed) + ' node(s)')
if missing:
    print('[wiring-fix] not found in /project1: ' + str(missing))
print('[wiring-fix] now reload each updated node (or save + reopen .toe)')
