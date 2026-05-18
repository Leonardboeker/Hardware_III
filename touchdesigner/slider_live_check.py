"""Live slider check - prints compute_state slider values once.

Run this AFTER moving the slider to a known position.
Compare the printed value to what you expect at that position.
"""

cs = op('/project1/compute_state')
if cs is None:
    print('FAIL: compute_state not found')
else:
    sr = cs['slider_raw'][0]
    psr = cs['phase_slider_raw'][0]
    fl = int(cs['floor'][0])
    pi = int(cs['phase_index'][0])
    sa = int(cs['slider_alive'][0])
    psa = int(cs['phase_slider_alive'][0])
    ws = int(cs['wrapper_state'][0])
    mid = int(cs['method_id'][0])

    print('=' * 50)
    print('SLIDER A (HEIGHT, GPIO34)')
    print('=' * 50)
    print('  Position (raw 0..1) : {:.3f}  ({:.0f}% travel)'.format(sr, sr*100))
    print('  Quantized FLOOR     : ' + str(fl) + ' / 5')
    print('  Alive (Serial tick) : ' + ('YES' if sa else 'NO'))
    print('')
    print('=' * 50)
    print('SLIDER B (BUILDING_PHASE, GPIO35)')
    print('=' * 50)
    print('  Position (raw 0..1) : {:.3f}  ({:.0f}% travel)'.format(psr, psr*100))
    print('  Quantized PHASE     : ' + str(pi) + ' / 5  (n_phases default)')
    print('  Alive (Serial tick) : ' + ('YES' if psa else 'NO'))
    print('  MANUAL_OVERRIDE     : ' + ('ACTIVE (10s countdown)' if ws else 'inactive (closed-loop)'))
    print('')
    print('  method_id           : ' + str(mid))
    print('')
    print('--- Expected mapping (default n_phases=5, MAX_FLOORS=5) ---')
    print('  raw 0.00 - 0.12 -> FLOOR 1 / PHASE 1')
    print('  raw 0.13 - 0.37 -> FLOOR 2 / PHASE 2')
    print('  raw 0.38 - 0.62 -> FLOOR 3 / PHASE 3')
    print('  raw 0.63 - 0.87 -> FLOOR 4 / PHASE 4')
    print('  raw 0.88 - 1.00 -> FLOOR 5 / PHASE 5')
