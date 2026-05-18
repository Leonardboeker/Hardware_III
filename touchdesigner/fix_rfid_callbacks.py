"""Fix the rfid_in Serial DAT 'Cannot find function: onReceive' error.

The Serial DAT's `par.callbacks` parameter points to a DAT containing the
callback functions (onReceive, onConnect, onDisconnect). The error means
either the linked DAT has a syntax error or doesn't define onReceive.
"""

import pathlib

print('=' * 60)
print('Inspect rfid_in callbacks chain')
print('=' * 60)

rfid = op('/project1/rfid_in')
if rfid is None:
    print('FAIL: /project1/rfid_in not found')
else:
    print('rfid_in type: ' + str(rfid.type))
    print('rfid_in par.callbacks raw: ' + str(rfid.par.callbacks))
    cb_dat = rfid.par.callbacks.eval()
    if cb_dat is None:
        print('FAIL: par.callbacks resolves to None')
    else:
        print('callbacks DAT name: ' + cb_dat.name + ' (type=' + str(cb_dat.type) + ')')
        text = cb_dat.text
        print('callbacks DAT text length: ' + str(len(text)))
        print('starts with BOM: ' + str(text.startswith('﻿')))
        print('first 80 chars: ' + repr(text[:80]))
        print('has "def onReceive": ' + str('def onReceive' in text))
        print('has "def onConnect": ' + str('def onConnect' in text))

    # Force-reload fresh from worktree
    src = pathlib.Path('D:/IAAC/Hardware_III/.claude/worktrees/objective-leakey-a3a366/touchdesigner/scripts/serial_rfid_v1.py')
    if not src.exists():
        print('FAIL: source file not found at ' + str(src))
    else:
        raw = src.read_bytes()
        if raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]
            print('stripped BOM from source')
        text = raw.decode('utf-8')

        # Push fresh content into BOTH callback DATs in case there is ambiguity
        for dat_name in ['serial1_callbacks', 'rfid_serial_callbacks']:
            dat = op('/project1/' + dat_name)
            if dat is None:
                continue
            if hasattr(dat.par, 'syncfile'):
                dat.par.syncfile = False
            dat.text = text
            # Toggle module to force re-evaluation
            if hasattr(dat.par, 'module'):
                try:
                    dat.par.module = False
                    dat.par.module = True
                except Exception:
                    pass
            print('wrote ' + str(len(text)) + ' bytes into ' + dat_name + ' and toggled module')

        # Make sure rfid_in callbacks points to one of these
        target = op('/project1/serial1_callbacks') or op('/project1/rfid_serial_callbacks')
        if target is not None:
            rfid.par.callbacks = target
            print('set rfid_in.par.callbacks -> ' + target.path)

print('')
print('=' * 60)
print('Re-test callback link')
print('=' * 60)
cb_dat = rfid.par.callbacks.eval()
if cb_dat is not None:
    print('callbacks now points to: ' + cb_dat.path)
    print('has "def onReceive": ' + str('def onReceive' in cb_dat.text))
