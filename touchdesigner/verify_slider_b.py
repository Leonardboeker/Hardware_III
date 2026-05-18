"""Verify Slider B integration is live in compute_state and serial_rfid_v1."""

print('=' * 60)
print('Verify Slider B integration')
print('=' * 60)

cs = op('/project1/compute_state')
if cs is None:
    print('FAIL: compute_state not found')
else:
    chans = [c.name for c in cs.chans('*')]
    print('compute_state has ' + str(len(chans)) + ' channels:')
    for c in chans:
        print('  ' + c)

    needed_a = ['floor', 'slider_raw', 'slider_alive']
    needed_b = ['phase_slider_raw', 'phase_index', 'phase_slider_alive', 'wrapper_state']

    missing_a = [c for c in needed_a if c not in chans]
    missing_b = [c for c in needed_b if c not in chans]

    print('')
    if missing_a:
        print('FAIL Slider A channels missing: ' + str(missing_a))
    else:
        print('OK Slider A channels: ' + str(needed_a))
    if missing_b:
        print('FAIL Slider B channels missing: ' + str(missing_b))
    else:
        print('OK Slider B channels: ' + str(needed_b))

print('')
print('--- live channel values ---')
if cs is not None:
    for name in ['method_id', 'floor', 'slider_raw', 'slider_alive',
                 'phase_slider_raw', 'phase_index', 'phase_slider_alive', 'wrapper_state']:
        try:
            v = cs[name][0]
            print('  ' + name.ljust(20) + ' = ' + str(v))
        except Exception as e:
            print('  ' + name.ljust(20) + ' MISSING (' + str(e) + ')')

print('')
print('--- rfid_in Serial DAT storage ---')
rfid = op('/project1/rfid_in')
if rfid is None:
    print('FAIL: rfid_in not found')
else:
    for key in ['method_id', 'floor', 'slider_raw', 'slider_last_frame',
                'phase_slider_raw', 'phase_slider_last_frame']:
        try:
            v = rfid.fetch(key, '<not stored>')
            print('  ' + key.ljust(25) + ' = ' + str(v))
        except Exception as e:
            print('  ' + key.ljust(25) + ' ERROR ' + str(e))
