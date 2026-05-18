"""Diagnose + fix: text_bar_bottom_status Text TOP not updating.

Symptom: panel_text.bar_bottom_status() returns correct text in Python,
but the Text TOP in the network shows stale content. Probably static text
in the Text TOP's Text parameter (vs a python expression).
"""

print('=' * 60)
print('Inspect text_bar_bottom_status Text TOP')
print('=' * 60)

tt = op('/project1/text_bar_bottom_status')
if tt is None:
    print('FAIL: text_bar_bottom_status not found')
else:
    print('Type: ' + str(tt.type))
    # The text TOP's text comes from par.text (usually) or from a CHOP
    if hasattr(tt.par, 'text'):
        cur = tt.par.text.val
        mode = tt.par.text.mode
        print('par.text current value (first 100 chars): ' + repr(cur[:100]))
        print('par.text mode: ' + str(mode))

    # Set the text param to a python expression so it auto-evaluates each cook
    expression = "op('panel_text').module.bar_bottom_status()"
    if hasattr(tt.par, 'text'):
        try:
            tt.par.text.expr = expression
            tt.par.text.mode = ParMode.EXPRESSION
            print('SET par.text expression -> ' + expression)
            print('Mode set to EXPRESSION')
        except Exception as e:
            print('FAIL setting expression: ' + str(e))
            # Fallback: write current bar_bottom_status() result as static text
            try:
                bb = op('/project1/panel_text').module.bar_bottom_status()
                tt.par.text = bb
                print('Fallback: wrote static text "' + bb + '"')
            except Exception as e2:
                print('Fallback also failed: ' + str(e2))

    # Force cook
    try:
        tt.cook(force=True)
        print('OK cooked text_bar_bottom_status')
    except Exception as e:
        print('FAIL cook: ' + str(e))

    # Render footprint reads from the Text TOP, so it also needs to cook
    rf = op('/project1/render_footprint')
    if rf is not None:
        try:
            rf.cook(force=True)
            print('OK cooked render_footprint')
        except Exception:
            pass

print('')
print('=' * 60)
print('Also fix the other text_* TOPs that show stale content')
print('=' * 60)

# Map other panel_text functions to their corresponding Text TOPs
panel_function_map = {
    'text_top_phase_navigation':  "op('panel_text').module.top_phase_navigation()",
    'text_left_info':             "op('panel_text').module.left_info()",
    'text_method_selection':      "op('panel_text').module.method_selection()",
    'text_right_comparison':      "op('panel_text').module.right_comparison()",
    'text_right_cost_chart':      "op('panel_text').module.right_cost_chart()",
    'text_right_phase_preview':   "op('panel_text').module.right_phase_preview()",
    'text_left_assembly_sequence':"op('panel_text').module.left_assembly_sequence()",
}

for top_name, expr in panel_function_map.items():
    t = op('/project1/' + top_name)
    if t is None:
        continue
    if hasattr(t.par, 'text'):
        try:
            t.par.text.expr = expr
            t.par.text.mode = ParMode.EXPRESSION
            print('OK ' + top_name + ' -> ' + expr)
        except Exception as e:
            print('FAIL ' + top_name + ': ' + str(e))

print('')
print('Final check (Slider B at current position):')
try:
    bb = op('/project1/panel_text').module.bar_bottom_status()
    print('  bar_bottom_status() => ' + bb)
except Exception as e:
    print('  bar_bottom_status() FAIL: ' + str(e))
