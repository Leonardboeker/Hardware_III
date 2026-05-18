"""Revert the Text TOP expressions I forced. Restores Onur's original setup.

Only keeps text_bar_bottom_status with my expression (that's the one we need
for Slider B FLOOR/PHASE display). All other text TOPs get their text mode
reset to CONSTANT (static) — they'll keep whatever they currently show.
"""

# These are the TOPs I overrode. Reset all to constant mode (static text).
overridden = [
    'text_top_phase_navigation',
    'text_left_info',
    'text_method_selection',
    'text_right_comparison',
    'text_right_cost_chart',
    'text_right_phase_preview',
    'text_left_assembly_sequence',
]

print('Reverting Text TOPs to CONSTANT mode...')
for name in overridden:
    t = op('/project1/' + name)
    if t is None:
        continue
    try:
        # Get current evaluated value, then bake it as static
        cur = t.par.text.eval()
        t.par.text.mode = ParMode.CONSTANT
        t.par.text = cur if cur else ''
        print('  OK ' + name + '  (frozen as static)')
    except Exception as e:
        print('  FAIL ' + name + ': ' + str(e))

print('')
print('Keeping text_bar_bottom_status as EXPRESSION (needed for live FLOOR/PHASE)...')
tt = op('/project1/text_bar_bottom_status')
if tt is not None:
    try:
        tt.par.text.expr = "op('panel_text').module.bar_bottom_status()"
        tt.par.text.mode = ParMode.EXPRESSION
        print('  OK text_bar_bottom_status -> live expression')
    except Exception as e:
        print('  FAIL: ' + str(e))

# Force re-cook everything text-driven
for n in overridden + ['text_bar_bottom_status', 'render_footprint']:
    op_node = op('/project1/' + n)
    if op_node is not None:
        try:
            op_node.cook(force=True)
        except Exception:
            pass

print('')
print('Done. UI should look like Onurs setup again, but text_bar_bottom_status now updates live.')
