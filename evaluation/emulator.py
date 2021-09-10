import os
import subprocess
from time import sleep

emulator_process = None
command = ['emulator', '-ports', ' 5554,5555', '-avd', "emulator1", '-no-audio',
           '-no-window',
           '-no-snapshot-load'
           ]


def start_emulator():
    global emulator_process
    if emulator_process is not None:
        emulator_process.kill()
        sleep(10)
    emulator_process = subprocess.Popen(command, universal_newlines=True,
                                        # cwd='/Users/usiusi/Library/Android/sdk/emulator/',
                                        stderr=subprocess.STDOUT,
                                        preexec_fn=os.setsid)
    sleep(30)
    print('Emulator Started')
