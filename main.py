#!/usr/bin/python3

import os
import sys
import getpass
import platform
import threading
from time import sleep
from pretty import title
from dataclasses import dataclass
from tkinter.filedialog import askopenfile, askdirectory

@dataclass
class BooleanVar: value: bool

def getpwd(string: str = '[ PASS ] \033[94mPassword: \033[0m') -> None:
    
    show = input('[ PASS ] \033[94mLeave blank to hide input: \033[0m').strip()
    
    if show: return input(string)
    return getpass.getpass(string)

def work(var = BooleanVar, frames = ['.  ', '.. ', '...', '   ']) -> None:
    n, i = len(frames), 0
    
    while 1:
        print('\r' + frames[i % n], end = '')
        
        sleep(.3)
        i += 1
        
        # Break
        if not var.value: break
        
    # Erase
    print('\r' + ' ' * 5)

def main(exe: str, action: str) -> None:
    '''
    Attempt to decrypt an archive.
    '''
    
    # Get source, target and password
    if len(sys.argv) >= 3: _, source, target, *args = sys.argv
    else:
        source, target, args = askopenfile('r').name, askdirectory(), []
        if not 'd' in action: source, target = target, source
    
    pwd = args[0] if len(args) else getpwd()
    
    # Debug
    print(f'[ BWF2 ] \033[93mStarting action:')
    print(' ' * 9 + f'\033[93mSource:\033[0m {source}')
    print(' ' * 9 + f'\033[93mTarget:\033[0m {target}')
    
    try:
        # Start to wait
        working = BooleanVar(True)
        threading.Thread(target=work, args = [working]).start()
        
        # Start decryption
        if 'd' in action:
            res = os.popen(f'{exe} x {source} -o"{target}" -p"{pwd}"').read()
        
        else:
            res = os.popen(f'{exe} a {source} -o"{target}" -m0=Copy -p"{pwd}"').read()
        
        # Stop waiting
        working.value = False
        
        # Make sure there is no error
        if 'Everything is Ok' in res: print('[ BWF2 ] \033[92mSuccessfully decrypted files.\033[0m')
        else: raise Exception(res)

    except Exception as e:
        # Error handling
        print(f'[ BWF2 ] Failed to decrypt files. Got error:\n\033[91m{e}\033[0m')
        working.value = False

if __name__ == '__main__':
    
    title('Started BWF2', 'DD', 93)
        
    print('[ BWF2 ] \033[93mStarted process.\033[0m')
    
    # Get action
    if len(sys.argv) >= 2 and sys.argv[1] in 'de': action = sys.argv.pop(1)
    else: exit('[ BWF2 ] Invalid format.')
    
    # Executable path (on linux, refers to the 7-zip AUR package)
    exe = {
        'Windows':  'C:/"Program Files"/7-Zip/7z.exe',
        'Linux':    '7-zip'
    }
    
    # Main
    main(exe[platform.system()], action)
