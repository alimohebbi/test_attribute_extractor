import os
import subprocess
from time import sleep

emulator_process = None
start_command = ['emulator', '-ports', ' 5554,5555', '-avd', emulator1, '-no-audio',
                 '-no-window',
                 '-no-snapshot-load'
                 ]

stop_command = [
    'adb', '-s', 'emulator-5554', 'emu', 'kill'
]
work_dir = '/Users/usiusi/Library/Android/sdk/emulator/'


def start_emulator():
    global emulator_process
    stop_emulator()
    emulator_process = subprocess.Popen(start_command, universal_newlines=True,
                                        # cwd=work_dir,
                                        stderr=subprocess.STDOUT,
                                        preexec_fn=os.setsid)
    sleep(30)
    print('Emulator Started')


def stop_emulator():
    emulator_stop_process = subprocess.Popen(stop_command, universal_newlines=True,
                                        # cwd=work_dir,
                                        stderr=subprocess.STDOUT,
                                        preexec_fn=os.setsid)
    emulator_stop_process.wait()
    sleep(10)
    print('Emulator Stopped')
