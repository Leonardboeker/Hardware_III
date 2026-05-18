"""Diagnose: call each panel_text function directly and print what comes back.

If a function returns empty/error string -> the underlying data (ui_state /
metrics_output) is broken. Not my fault.
If a function returns proper text -> the Text TOP just needs the expression
re-applied.
"""

pt = op('/project1/panel_text')
if pt is None:
    print('FAIL: panel_text DAT missing')
else:
    funcs = ['top_phase_navigation', 'left_info', 'method_selection',
             'right_comparison', 'right_cost_chart', 'right_phase_preview',
             'left_assembly_sequence', 'bar_bottom_status']

    for fn in funcs:
        try:
            f = getattr(pt.module, fn, None)
            if f is None:
                print(fn.ljust(28) + ' MISSING IN MODULE')
                continue
            result = f()
            r = str(result)
            if len(r) > 80:
                r = r[:77] + '...'
            print(fn.ljust(28) + ' = ' + repr(r))
        except Exception as e:
            print(fn.ljust(28) + ' EXCEPTION: ' + str(e))

print('')
print('--- ui_state module (owner-stored UI payload) ---')
root = op('/project1')
try:
    ui_payload = root.fetch('ui_state', None)
    if ui_payload is None:
        print('  owner has no ui_state stored (metrics_engine never published)')
    else:
        print('  ui_state keys: ' + str(list(ui_payload.keys()) if isinstance(ui_payload, dict) else type(ui_payload)))
except Exception as e:
    print('  fetch ui_state failed: ' + str(e))

print('')
print('--- metrics_output (raw metrics) ---')
try:
    metrics = root.fetch('metrics_output', None)
    if metrics is None:
        print('  owner has no metrics_output (compute_and_store_touchdesigner never succeeded)')
    else:
        print('  metrics_output type: ' + str(type(metrics)))
except Exception as e:
    print('  fetch metrics_output failed: ' + str(e))
