"""TD wiring fix — repoints all hardcoded File-Sync paths to relative paths.

Run from TouchDesigner textport (Alt+T):

    exec(open('D:/IAAC/Hardware_III/touchdesigner/wiring_fix.py').read())

The .toe file lives in the repo root, so relative paths like
'touchdesigner/scripts/panel_text.py' resolve correctly on any machine.

After running, hit Save (Ctrl+S) on the .toe so the fixed paths persist.
"""

mappings = {
    'panel_text':                 'touchdesigner/scripts/panel_text.py',
    'methods_db':                 'data/methods_db.json',
    'script2_callbacks':          'touchdesigner/scripts/state_chop_v1.py',
    'metrics_engine':             'touchdesigner/scripts/metrics_engine.py',
    'bootstrap_metric_ui':        'touchdesigner/scripts/metric_ui_bootstrap.py',
    'ui_state':                   'touchdesigner/scripts/ui_state.py',
    'lca_data':                   'touchdesigner/scripts/lca_data_reader.py',
    'lca_data_callbacks':         'touchdesigner/scripts/lca_data_reader.py',
    'rfid_serial_callbacks':      'touchdesigner/scripts/serial_rfid_v1.py',
    'serial1_callbacks':          'touchdesigner/scripts/serial_rfid_v1.py',
    'compute_state_callbacks':    'touchdesigner/scripts/vision2_state_chop.py',
    'vision2_state_callbacks':    'touchdesigner/scripts/vision2_state_chop.py',
    'render_footprint_callbacks': 'touchdesigner/scripts/footprint_viz_v5.py',
    'method_preview_masonry':     'touchdesigner/assets/method_loops/masonry_mode.gif',
    'method_preview_3d_printed':  'touchdesigner/assets/method_loops/3d_printed_mode.gif',
    'method_preview_prefab':      'touchdesigner/assets/method_loops/prefab_mode.gif',
}

fixed = 0
missing = []
for name, rel in mappings.items():
    nodes = op('/project1').findChildren(name=name, depth=20)
    if not nodes:
        missing.append(name)
        continue
    for n in nodes:
        if hasattr(n.par, 'file'):
            n.par.file = rel
            if hasattr(n.par, 'syncfile'):
                n.par.syncfile = True
            fixed += 1
            print(f'  -> {n.path}  file = {rel}')

print(f'[wiring-fix] updated {fixed} node(s)')
if missing:
    print(f'[wiring-fix] not found in /project1: {missing}')
print('[wiring-fix] now reload each updated node (or save + reopen .toe)')
