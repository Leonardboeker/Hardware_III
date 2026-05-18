"""Make Text TOPs reactive — defensive version.

Strategy:
1. For each Text TOP, call its function and check result is non-trivial
2. If function returns < 5 chars or contains 'error'/'exception', SKIP it
3. Only set expression for TOPs where the function output is rich
4. Print expected output for each so user can sanity-check

If anything looks bad in UI after running: close TD without save,
reopen .10.toe (or vertical-slice.GOOD-BASELINE-AUTO.toe).
"""

mappings = {
    'text_top_phase_navigation':   'top_phase_navigation',
    'text_left_info':              'left_info',
    'text_method_selection':       'method_selection',
    'text_right_comparison':       'right_comparison',
    'text_right_cost_chart':       'right_cost_chart',
    'text_right_phase_preview':    'right_phase_preview',
    'text_left_assembly_sequence': 'left_assembly_sequence',
    'text_bar_bottom_status':      'bar_bottom_status',
}

print('=' * 60)
print('Snapshot current Text TOP states')
print('=' * 60)
snapshot = {}
for top_name in mappings.keys():
    t = op('/project1/' + top_name)
    if t is None:
        continue
    try:
        snapshot[top_name] = {
            'text': t.par.text.val,
            'mode': t.par.text.mode,
            'expr': t.par.text.expr,
        }
    except Exception:
        pass
print('snapshotted ' + str(len(snapshot)) + ' Text TOPs')

print('')
print('=' * 60)
print('Verify panel_text function outputs (sanity check)')
print('=' * 60)
ok_to_set = []
for top_name, fn_name in mappings.items():
    try:
        result = getattr(op('/project1/panel_text').module, fn_name)()
        result_str = str(result)
        if not result_str or len(result_str.strip()) < 5:
            print('  SKIP ' + top_name + '  (function returned empty: ' + repr(result_str[:40]) + ')')
            continue
        if 'error' in result_str.lower() or 'exception' in result_str.lower():
            print('  SKIP ' + top_name + '  (function returned error-like: ' + repr(result_str[:40]) + ')')
            continue
        preview = result_str.replace('\n', '\\n')
        if len(preview) > 60:
            preview = preview[:57] + '...'
        print('  OK   ' + top_name.ljust(32) + ' = ' + preview)
        ok_to_set.append((top_name, fn_name))
    except Exception as e:
        print('  SKIP ' + top_name + '  (function raised: ' + str(e) + ')')

print('')
print('=' * 60)
print('Set ' + str(len(ok_to_set)) + ' Text TOPs as live expressions')
print('=' * 60)
for top_name, fn_name in ok_to_set:
    t = op('/project1/' + top_name)
    if t is None:
        continue
    try:
        t.par.text.expr = "op('panel_text').module." + fn_name + "()"
        t.par.text.mode = ParMode.EXPRESSION
        t.cook(force=True)
        print('  -> ' + top_name)
    except Exception as e:
        print('  FAIL ' + top_name + ': ' + str(e))

# Force render_footprint to recook so blits pick up new text content
rf = op('/project1/render_footprint')
if rf is not None:
    rf.cook(force=True)

print('')
print('DONE. Try: tap a different RFID tag and see if YOUR SELECTION etc. update.')
print('If UI looks broken: close TD WITHOUT save, reopen .10.toe.')
