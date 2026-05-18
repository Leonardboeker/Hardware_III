"""Point compute_state Script CHOP at the new vision2_state_chop.py."""

cs = op('/project1/compute_state')
if cs is None:
    print('FAIL: compute_state not found')
else:
    print('compute_state current state:')
    print('  type=' + str(cs.type))
    # List relevant parameters
    for par_name in ['callbacks', 'file', 'syncfile', 'script', 'text']:
        if hasattr(cs.par, par_name):
            try:
                v = getattr(cs.par, par_name).eval()
                print('  par.' + par_name + ' = ' + str(v))
            except Exception:
                print('  par.' + par_name + ' present (no eval)')

    # Approach 1: Point callbacks at vision2_state_callbacks DAT
    target_dat = op('/project1/vision2_state_callbacks')
    if target_dat is None:
        print('FAIL: vision2_state_callbacks DAT not found')
    else:
        print('vision2_state_callbacks DAT text length: ' + str(len(target_dat.text)))

        # Try: set callbacks DAT pointer
        if hasattr(cs.par, 'callbacks'):
            try:
                cs.par.callbacks = target_dat
                print('OK set par.callbacks to vision2_state_callbacks')
            except Exception as e:
                print('FAIL par.callbacks: ' + str(e))

        # Approach 2: Write the .py content directly into compute_state's inline script
        # Script CHOPs can also use the DAT named after the CHOP itself.
        # Let us also force-update the inline script.
        try:
            cs.text = target_dat.text
            print('OK wrote vision2_state_chop.py source into compute_state.text')
        except Exception as e:
            print('SKIP cs.text not writable: ' + str(e))

        # Force cook
        try:
            cs.cook(force=True)
            print('OK cooked compute_state')
        except Exception as e:
            print('FAIL cook: ' + str(e))

    # Verify channel count
    chans = [c.name for c in cs.chans('*')]
    print('compute_state now has ' + str(len(chans)) + ' channels:')
    for c in chans:
        print('  ' + c)
