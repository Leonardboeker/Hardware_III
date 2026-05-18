"""Make all panel text TOPs live-reactive by setting their text param as
expressions that call the corresponding panel_text function.

panel_text functions already return correct content (verified via diag).
Just need the Text TOPs to evaluate them every cook.
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

print('Setting Text TOPs as live expressions...')
ok = 0
fails = []
for top_name, fn_name in mappings.items():
    t = op('/project1/' + top_name)
    if t is None:
        fails.append(top_name + ' (missing)')
        continue
    try:
        # First verify the function actually returns something useful
        result = getattr(op('/project1/panel_text').module, fn_name)()
        if not result or len(str(result).strip()) < 2:
            fails.append(top_name + ' (function returned empty)')
            continue

        expr = "op('panel_text').module." + fn_name + "()"
        t.par.text.expr = expr
        t.par.text.mode = ParMode.EXPRESSION
        t.cook(force=True)
        ok += 1
        preview = str(result).replace('\n', '\\n')
        if len(preview) > 60:
            preview = preview[:57] + '...'
        print('  OK ' + top_name.ljust(32) + ' = ' + preview)
    except Exception as e:
        fails.append(top_name + ' (' + str(e) + ')')

print('')
print(str(ok) + ' / ' + str(len(mappings)) + ' text TOPs now live-reactive')
if fails:
    print('Failed: ' + str(fails))

# Force re-cook render_footprint so the new text TOPs get blitted
rf = op('/project1/render_footprint')
if rf is not None:
    rf.cook(force=True)
    print('render_footprint cooked')
