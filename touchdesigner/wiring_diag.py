"""TD diagnostic - finds where named nodes live in the project tree.

Run from TouchDesigner textport (Alt+T):

    exec(open('D:/IAAC/Hardware_III/touchdesigner/wiring_diag.py').read())
"""

NAMES = [
    'panel_text', 'methods_db', 'metrics_engine', 'bootstrap_metric_ui',
    'ui_state', 'lca_data', 'compute_state', 'rfid_in', 'vision_in',
    'render_footprint', 'method_preview_masonry', 'script2_callbacks',
]

print('--- searching from root (/) with depth=50 ---')
for name in NAMES:
    hits = op('/').findChildren(name=name, depth=50)
    if hits:
        for h in hits:
            t = h.type if hasattr(h, 'type') else '?'
            print('  FOUND ' + name + '  type=' + str(t) + '  path=' + h.path)
    else:
        print('  MISSING ' + name)

print('--- top-level containers in / ---')
try:
    for child in op('/').children:
        print('  ' + child.path + '  (type=' + str(child.type) + ')')
except Exception as e:
    print('  error listing / children: ' + str(e))
