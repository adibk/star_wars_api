#
# Swapi, the Star Wars API
#
#
# Documentation API
# https://swapi.dev/documentation#root
#
# The Base URL for swapi is:
# https://swapi.dev/api/
# 
# /api/<resource>/schema
#

import requests
import json
import sys
from itertools import zip_longest


# Get the arguments from command line
############################
args = sys.argv
#############################


# API ressources available as of 2024-03-01
############################
api_ressources = ('peoples', 'planetss', 'films', 'species', 'vehicles', 'starships')
#############################


#
# Terminal Colors
#

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
    
def str_clr(s, clr=Color.RED):
    return clr + s + Color.END

def clr(lst, clr=Color.RED):
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

# 
# Tools
# 

def safe_max(l, default=None):
    if not l:
        return default
    return max(l)

def max_len(l):
    return safe_max([len(i) for i in l], 0)

def max_lists(*lists):
    ret = 0
    for l in lists:
        ret = max(ret, max_len(l))
    return ret

def if_none(val, new_val):
    return val if val != None else new_val


#
# URLs
#

#############################
url = 'https://swapi.dev/api/'
#############################

def get_url(ressource, schema):
    return url + ressource + '/' + str(schema)

def get_url_search(ressource, schema):
    return url + ressource + '/?search=' + schema

#
# Convert and print
#

def str_to_json(str):
    if str is not None:
        df = json.loads(str)    
    else:
        return None
    return df

def print_data_str(str):
    if str is not None:
        df = str_to_json(str)    
        print(json.dumps(df, indent=4))
    else:
        print("String is empty.")
        return None
    return df

def print_data(df):
    print(json.dumps(df, indent=4))

def r_aligh(s, len):
    return f'{s:<{len}}'

def print_diff(diff):
    msgs = ["Expecting:",
           "But Getting:"]
    none_msg = '<None>'
    spaces = 10
    max_len = max(max_lists(diff[0], diff[1]), len(msgs[0]), len(msgs[1]), len(none_msg))
    clr_msgs = clr([r_aligh(msg, max_len) for msg in msgs], [Color.BRIGHT_GREEN, Color.BRIGHT_RED])
    
    print(f'\n{r_aligh(clr_msgs[0], max_len)}{"":{spaces}}{clr_msgs[1]}\n')
    for rsrc_1, rsrc_2 in zip_longest(diff[0], diff[1]):
        rsrc_1 = if_none(rsrc_1, clr(r_aligh(none_msg, max_len), Color.BRIGHT_BLACK))
        rsrc_2 = if_none(rsrc_2, clr(r_aligh(none_msg, max_len), Color.BRIGHT_BLACK))
        print(f'{r_aligh(rsrc_1, max_len)}{"":{spaces}}{rsrc_2}')
    print('\n')


#
# Fetch from api string data, http request
#
 
def fetch_data(url, to_json=True):
    try:
        # Get request timeout of 5 seconds
        response = requests.get(url, timeout=5)
        
        # Check the status code
        response.raise_for_status()
        
        return str_to_json(response.text)
    except requests.RequestException as e:
        # errors (e.g., connection refused, timeout exceeded, etc.)
        print(f"An HTTP request error occurred: {e}")
        return None


#
# Ressources (planets, people, ...)
#

def get_ressources_df():
    df = fetch_data(url)
    return df

#############################
ressources_df = get_ressources_df()
#############################

def get_ressources():
    ressource = ()
    for item in ressources_df:
            ressource += (item, )
    return ressource

def sort_tuple(tup):
    return tuple(sorted(tup))

#############################
ressources = get_ressources()
ressources_to_check = api_ressources
#############################

def pretty_tuple(tup):
    output = ', '.join(str(item) for item in tup)
    return output

def diff_rsrc(rsrc_1, rsrc_2):
    diff_1 = set(rsrc_1) - set(rsrc_2)
    diff_2 = set(rsrc_2) - set(rsrc_1)
    return (sort_tuple(diff_1), sort_tuple(diff_2))

def check_ressources():
    rsrc_to_check_sorted = sort_tuple(ressources_to_check)
    rsrc_sorted = sort_tuple(ressources)
    if  rsrc_to_check_sorted == rsrc_sorted:
        print("Ressources are up-to-date")
        return True
    else:
        print("!!WARNING!! - Ressources are not up to date")
        # print("\nExpected:")
        # print(pretty_tuple(rsrc_sorted))
        # print("\nBut getting: ")
        # print(pretty_tuple(rsrc_to_check_sorted))
        diff = diff_rsrc(rsrc_sorted, rsrc_to_check_sorted)
        print_diff(diff)
    return False

#
# Handling specific data
# Ressources from base
# Planets
# Make a seach
#

def get_planet(n):
    df = fetch_data(get_url("planets", n))
    return df

def search(ressource, s):
    df = fetch_data(get_url_search(ressource, s))
    return df


#
# Handling arguments
#
   
def switch_case(main_args):
    case = main_args[1]
    if case == 'ressources':
        return get_ressources_df()
    elif case == 'planet':
        return get_planet(main_args[2])
    elif case == 'search':
        if len(main_args) > 3:
            return search(main_args[2], main_args[3])
        else:
            print("Search missing argument")
    elif case == 3:
        pass
    else:
        print("Wrong ressource")
    return None
    
def handle_args(elems):
    if len(elems) > 1:
        if len(elems) > 2 or elems[1] == "ressources":
            data = switch_case(elems) 
            if data is not None:
                print_data(data)
            else:
                print("No Data")
        else:
            print("Pass schema")
    else:
        print("Pass ressource")
  

#
# Main
#
    
def main():
    print("")
    check_ressources()
    handle_args(args)
    print("\n")
    
if __name__ == "__main__":
    main()
    
