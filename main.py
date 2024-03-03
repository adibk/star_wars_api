#################################################################################################################################
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
#################################################################################################################################

import requests
import json
import sys
from itertools import zip_longest

from utils import colors
from utils import tools

# Get the arguments from command line
############################
args = sys.argv
#############################


# API ressources available as of 2024-03-01
############################
api_ressources = ('people', 'planets', 'films', 'spedcies', 'vehicles', 'starships')
#############################


##################################################################################################################################
# URLs
##################################################################################################################################

#############################
url = 'https://swapi.dev/api/'
#############################

def get_url(ressource, schema):
    return url + ressource + '/' + str(schema)

def get_url_search(ressource, schema):
    return url + ressource + '/?search=' + schema

##################################################################################################################################
# Convert and print
##################################################################################################################################

def NEW_LINE(n=0):
    print("\n" * n)

man = "py main.py <resource> <>"

def r_aligh(s, len):
    return f'{s:<{len}}'

def print_man(usage=None):
    if not usage:
        usage = man
    print(usage)

def print_err(err):
    print("Error:", err)
    print_man()

def print_warning(err):
    print("!!WARNING!! -", err)

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

def print_diff(diff):
    msgs = ["Expecting:",
           "But Getting:"]
    none_msg = '<None>'
    spaces = 10
    max_len = max(tools.max_lists(diff[0], diff[1]), len(msgs[0]), len(msgs[1]), len(none_msg))
    clr_msgs = colors.clr([r_aligh(msg, max_len) for msg in msgs], [colors.Color.BRIGHT_GREEN, colors.Color.BRIGHT_RED])
    
    print(f'\n{r_aligh(clr_msgs[0], max_len)}{"":{spaces}}{clr_msgs[1]}\n')
    for rsrc_1, rsrc_2 in zip_longest(diff[0], diff[1]):
        rsrc_1 = tools.if_none(rsrc_1, colors.clr(r_aligh(none_msg, max_len), colors.Color.BRIGHT_BLACK))
        rsrc_2 = tools.if_none(rsrc_2, colors.clr(r_aligh(none_msg, max_len), colors.Color.BRIGHT_BLACK))
        print(f'{r_aligh(rsrc_1, max_len)}{"":{spaces}}{rsrc_2}')
    print('\n')

def pretty_tuple(tup):
    output = ', '.join(str(item) for item in tup)
    return output

##################################################################################################################################
# Fetch from api string data, http request
##################################################################################################################################
 
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


##################################################################################################################################
# Ressources (planets, people, ...)
##################################################################################################################################

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

#############################
ressources = get_ressources()
ressources_to_check = api_ressources
#############################

def diff_rsrc(rsrc_1, rsrc_2):
    diff_1 = set(rsrc_1) - set(rsrc_2)
    diff_2 = set(rsrc_2) - set(rsrc_1)
    return (tools.sort_tuple(diff_1), tools.sort_tuple(diff_2))

def check_ressources(out=False, err=True):
    rsrc_to_check_sorted = tools.sort_tuple(ressources_to_check)
    rsrc_sorted = tools.sort_tuple(ressources)
    if  rsrc_to_check_sorted == rsrc_sorted:
        if out:
            print("Ressources are up-to-date")
        return True
    elif err:
        print_warning("Ressources are not up to date")
        # print("\nExpected:")
        # print(pretty_tuple(rsrc_sorted))
        # print("\nBut getting: ")
        # print(pretty_tuple(rsrc_to_check_sorted))
        diff = diff_rsrc(rsrc_sorted, rsrc_to_check_sorted)
        print_diff(diff)
    return False

##################################################################################################################################
#
# Handling specific data
# Ressources from base
# Planets
# Make a seach
#
##################################################################################################################################

def get_planet(n):
    df = fetch_data(get_url("planets", n))
    return df

def search(ressource, s):
    df = fetch_data(get_url_search(ressource, s))
    return df


##################################################################################################################################
# Handling arguments
##################################################################################################################################
   
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
            print_err("Search missing argument")
    elif case == 3:
        pass
    else:
        print_err("Wrong ressource")
    return None
    
def handle_args(elems):
    if len(elems) > 1:
        if len(elems) > 2 or elems[1] == "ressources":
            data = switch_case(elems) 
            if data is not None:
                print_data(data)
            else:
                print_err("No Data")
        else:
            print_err("Pass schema")
    else:
        print_err("Pass ressource")
  

##################################################################################################################################
# Main
##################################################################################################################################
    
def main():
    NEW_LINE()
    check_ressources()
    handle_args(args)
    NEW_LINE(2)
    
if __name__ == "__main__":
    main()
    
