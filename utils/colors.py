##################################################################################################################################
# Terminal Colors
##################################################################################################################################

class Color:
    # ANSI escape sequences for text colors
    END = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'  # Grey
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # ANSI escape sequences for text styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    STRIKETHROUGH = '\033[9m'
    
def str_clr(s, clr=Color.BRIGHT_RED):
    return clr + s + Color.END

def clr(lst, clr=Color.BRIGHT_RED):
    clr_lst = []
    if not isinstance(clr, list):
        clr = [clr]
    i = 0
    if isinstance(lst, list):
        for str in lst:
            clr_lst.append(clr[i % len(clr)] + str + Color.END)
            i += 1
        return clr_lst
    return str_clr(lst, clr[0])

