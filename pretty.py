from os import get_terminal_size

__BORDERS = {
    'L':    '─│┌┐└┘',   # Light
    'H':    '━┃┏┓┗┛',   # Heavy
    'D':    '┄┊┌┐└┘',   # Dashed
    'DD':   '═║╔╗╚╝',   # Double
    'LD':   '─║╓╖╙╜',   # Light Double
    'DL':   '═│╒╕╘╛',   # Double Light
    'F':    '██████',   # Full block
    'B':    ['$c'] * 6, # Red background
    None:   '      '    # No border
}

def title(msg: str, bdr: str = 'L', col: int = 0) -> None:
    '''
    Print out a message with a border in the console.
    
        msg: str <-> The message to print
        bdr: str <-> The type of the border (L, H, etc.)
        col: int <-> The ANSI foreground color code value
    '''
    
    # Build borders and color
    bd, cs, ce = __BORDERS[bdr], f'\033[{col}m', '\033[0m'
    bd = [f'{cs}{c}'.replace('$c', f'\033[4{str(col)[-1]}m ')
          if '$c' in c else f'{cs}{c}{ce}' for c in bd]
    
    # Build frame
    ctn = f"{msg: ^{get_terminal_size().columns - 2}}"
    sep = len(ctn) * bd[0]

    # Send
    print(f'{bd[2]}{sep}{bd[3]}\n{bd[1]}{ctn}{bd[1]}\n{bd[4]}{sep}{bd[5]}{ce}')




# EOF