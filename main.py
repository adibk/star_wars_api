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
import re
import random

from utils import colors
from utils.colors import Color
from utils import tools
from unittest import test
from unittest.test import TEST

# Get the arguments from command line
############################
args = sys.argv
#############################


# API resources available as of 2024-03-01
############################
api_resources = ('people', 'planets', 'films', 'species', 'vehicles', 'starships')
#############################


##################################################################################################################################
# Options
##################################################################################################################################

spe_args = ('info', 'resources', 'search')

user_opts = None

verbose = False
# verbose = True
no_color = False
# no_color = True
stream_out = True
# stream_err = False
stream_err = True
# stream_err = False


##################################################################################################################################
# URLs
##################################################################################################################################

#############################
url = 'https://swapi.dev/api/'
url = 'https://swapi.tech/api/'
url_documentation = f'{url}documentation'
#############################

def get_url(resource, schema=""):
    return url + resource + '/' + str(schema)

def get_url_search(resource, schema):
    return url + resource + '/?search=' + schema

##################################################################################################################################
# Convert and print
##################################################################################################################################


def NEW_LINE(n=0):
    print("\n" * n)

python_main = f"python{sys.version_info[0]} {args[0]}"
example_rsrc = f'{api_resources[1] if len(api_resources) > 1 else "<resource>"}'
man = f'''

{colors.clr("The Star Wars API", Color.UNDERLINE + Color.BOLD + Color.GREEN)}

{colors.clr("Usage", Color.UNDERLINE)}:
{colors.clr(python_main + " info", Color.BRIGHT_BLACK)}
{colors.clr(python_main + " resources", Color.BRIGHT_BLACK)}
{colors.clr(python_main + " <resource> <schema>", Color.BRIGHT_BLACK)}
{colors.clr(python_main + " search <resource> <search string>", Color.BRIGHT_BLACK)}

<resources> are: {tools.pretty_tuple(api_resources)}

{colors.clr("Examples", Color.UNDERLINE)}:
{colors.clr(python_main + " " + example_rsrc + " 3", Color.BRIGHT_BLACK)}
{colors.clr(python_main + " search " + example_rsrc + " hoth", Color.BRIGHT_BLACK)}
\n
'''

def r_aligh(s, len):
    return f'{s:<{len}}'

def print_man(usage=None):
    if not usage:
        usage = man
    print(usage)

err_occured = False

def print_err(err=None, man=True):
    global err_occured
    
    if stream_err == False:
        return
    if err is not None:
        print(colors.clr("Error:"), err)
    if man == True and err_occured == False:
        print_man()
    err_occured = True

def print_warning(err):
    print(print(colors.clr("!!WARNING!! -", Color.MAGENTA), err))

def str_to_json(str):
    if str is not None:
        df = json.loads(str)    
    else:
        return None
    return df

# def print_data_str(str):
#     if str is not None:
#         df = str_to_json(str)    
#         print(json.dumps(df, indent=4))
#     else:
#         print("String is empty.")
#         return None
#     return df

def print_data(data):
    # print(type(data))
    if isinstance(data, str):
        print(data)
    else:
        print(json.dumps(data, indent=4))

def print_diff(diff):
    msgs = ["Expecting:",
           "But Getting:"]
    none_msg = '<None>'
    
    spaces = 10
    max_len = max(tools.max_lists(diff[0], diff[1]), len(msgs[0]), len(msgs[1]), len(none_msg))
    
    clr_msgs = colors.clr([r_aligh(msg, max_len) for msg in msgs], [Color.BRIGHT_GREEN, Color.BRIGHT_RED])
    print(f'\n{r_aligh(clr_msgs[0], max_len)}{"":{spaces}}{clr_msgs[1]}\n')
    
    for rsrc_1, rsrc_2 in zip_longest(diff[0], diff[1]):
        rsrc_1 = tools.if_none(rsrc_1, colors.clr(r_aligh(none_msg, max_len), Color.BRIGHT_BLACK))
        rsrc_2 = tools.if_none(rsrc_2, colors.clr(r_aligh(none_msg, max_len), Color.BRIGHT_BLACK))
        print(f'{r_aligh(rsrc_1, max_len)}{"":{spaces}}{rsrc_2}')
    NEW_LINE()
    

##################################################################################################################################
# Fetch from api string data, http request
##################################################################################################################################
 
def fetch_data(url, to_json=True):
    try:
        # Get request timeout of 5 seconds
        response = requests.get(url, timeout=5)
        
        # Check the status code
        response.raise_for_status()
        if to_json == True:
            return str_to_json(response.text)
        return response.text
    except requests.RequestException as e:
        # errors (e.g., connection refused, timeout exceeded, etc.)
        print_err(f"An HTTP request error occurred: {e}")
        return None


##################################################################################################################################
# Resources (planets, people, ...)
##################################################################################################################################

def get_resources_df():
    df = fetch_data(url)
    return df

#############################
resources_df = get_resources_df()
#############################

def get_resources():
    resource = ()
    if resources_df == None:
        return None
    # change to this line in the 'https://swapi.dev/api/' api
    # for item in resources_df:
    for item in resources_df['result']:
            resource += (item, )
    return resource

#############################
resources_to_check = get_resources()
resources = api_resources
#############################

def diff_rsrc(rsrc_1, rsrc_2):
    diff_1 = set(rsrc_1) - set(rsrc_2)
    diff_2 = set(rsrc_2) - set(rsrc_1)
    return (tools.sort_tuple(diff_1), tools.sort_tuple(diff_2))

def check_resources(out=False, err=True):
    if resources_to_check == None:
        # might want to add a output, specially if verbose: Check haven't been possible
        return False

    rsrc_to_check_sorted = tools.sort_tuple(resources_to_check)
    rsrc_sorted = tools.sort_tuple(resources)
    if  rsrc_to_check_sorted == rsrc_sorted:
        if out == True:
            print("Resources are up-to-date")
        return True
    elif err == True:
        print_warning("Resources are not up to date")
        if out:
            print("\nExpected:")
            print(tools.pretty_tuple(rsrc_sorted))
            print("\nBut getting: ")
            print(tools.pretty_tuple(rsrc_to_check_sorted))
            NEW_LINE()
        diff = diff_rsrc(rsrc_sorted, rsrc_to_check_sorted)
        print_diff(diff)
    return False

##################################################################################################################################
#
# Handling specific data
# Resources from base
# Planets
# Make a seach
#
##################################################################################################################################

def get_people(n):
    df = fetch_data(get_url("people", n))
    # print(n)
    return df

def get_planets(n):
    df = fetch_data(get_url("planets", n))
    return df

def get_films(n):
    df = fetch_data(get_url("films", n))
    return df

def get_species(n):
    df = fetch_data(get_url("species", n))
    return df

def get_vehicles(n):
    df = fetch_data(get_url("vehicles", n))
    return df

def get_starships(n):
    df = fetch_data(get_url("starships", n))
    return df

def search(resource, s):
    df = fetch_data(get_url_search(resource, s))
    return df

def get_one_item(rsrc, n=1):
    # print(rsrc, n)
    df = fetch_data(get_url(rsrc, n))
    # print(n)
    return df

def get_rand_item(rsrc):
    n = random.randint(0, 20)
    return get_one_item(rsrc, n)
    
from selenium import webdriver
import time

def get_generated_data(url, timeout):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(timeout) 

    html = driver.page_source
    driver.quit()
    return html

    
def get_info(rsrc):
    df = tools.clean_str(fetch_data(url_documentation, False))
    df = get_generated_data(url_documentation, 3)
    print(df)
     
    info = f'{colors.clr(rsrc.capitalize(), Color.UNDERLINE + Color.BOLD + Color.GREEN)}\n\n'
    pattern = re.compile(rf'<h3>{rsrc}</h3><p>(.*?)</p>', re.IGNORECASE)
    match = re.search(pattern, df)
    if match:
        info += tools.strip_tags(match.group(1))
        info += f'{Color.BRIGHT_BLACK}\nFrom the Star Wars API - SWAPI - {colors.clr(url_documentation, Color.UNDERLINE)}{Color.END}'
    else:
        info += 'No Info\n'
    return info

def get_sample(rsrc, n):
    if n == 0:
        return None
    
    data = []
    n = n if n < 5 else 5
    unique_l = random.sample(range(1, 20), n)
    for i in unique_l:
        item = get_one_item(rsrc, i)
        if item is not None:
            data.append(get_one_item(rsrc, i))
    return data
    
def print_json_tree(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print(" " * indent + f'{colors.clr(str(key), Color.BRIGHT_WHITE + Color.BOLD)}')
            print_json_tree(value, indent + 4)
    elif isinstance(data, list):
        for item in data:
            print_json_tree(item, indent)
    else:
        print(" " * (indent + 4) + f'{colors.clr(str(data), Color.BRIGHT_BLUE + Color.ITALIC)}')

def get_struct(rsrc):
    data = get_one_item(rsrc)
    print_json_tree(data, 5)
    NEW_LINE()
    return None

# Do not work in the 'https://swapi.dev/api/' api
def get_properties(rsrc):
    data = get_one_item(rsrc)
    print_json_tree(data['result']['properties'], 5)
    NEW_LINE()
    return None

def get_keys(rsrc):
    data = get_one_item(rsrc)
    # change to this line in the 'https://swapi.dev/api/' api
    # for key in data.keys():
    for key in data['result']['properties'].keys():
        print(key)
    NEW_LINE()
    return None


def get_all(rsrc):
    next_url = get_url(rsrc)
    all_results = []

    # print(next_url)
    while next_url:
        data = fetch_data(next_url)
        # print(data)
        if data == None:
            print("End")
            break        
        all_results.extend(data['results'])

        next_url = data['next']
        
    return all_results

def get_all_split(rsrc):
    # pass 
    next_url = get_url(rsrc)
    all_results = []

    # print(next_url)
    while next_url:
        data = fetch_data(next_url)
        print_data(data)
        # TEST()
        s = input("continue Y/N: ")
        if s == 'N':
            break
        if data == None:
            print("End")
            break        
        all_results.extend(data['results'])

        next_url = data['next']
        
    return None



##################################################################################################################################
# Handling arguments
##################################################################################################################################

def switch_case(main_args):
    rsrc = main_args[1]
    
    if rsrc in spe_args:
        if rsrc == 'resources':
            return get_resources_df()
        elif rsrc == 'search':
            return search(main_args[2], main_args[3])
    
    case = main_args[2]
    pattern = re.compile(r'^[0-9]+$')
    
    if case == 'info':
        return get_info(rsrc)
    elif case == 'all':
        # return
        return get_all(rsrc)
    elif case == 'struct':
        return get_struct(rsrc)
    elif case == 'properties':
        return get_properties(rsrc)
    elif case == 'keys':
        return get_keys(rsrc)
    elif case == 'sample':
        return get_sample(rsrc, int(main_args[3]))
    elif case == 'rand':
        return get_rand_item(rsrc)
    elif case == 'all-split':
        return get_all_split(rsrc)
    elif  pattern.match(case):
        return get_one_item(rsrc, int(case))
    return None

def check_args(elems):
    nb_args = len(elems) - 1
    # no arg or arg=info
    if nb_args == 0 or (nb_args >= 0 and elems[1] == spe_args[0]):
        print_err()
    # check if arg 1 is resource, if ok then is there schema
    elif nb_args >= 1 and elems[1] not in spe_args:
        if elems[1] not in api_resources:
            print_err(f"Wrong resource {colors.clr(elems[1], Color.RED)}")
        elif nb_args == 1:
            print_err("Pass schema")
        elif nb_args == 2 and elems[2] == 'sample':
            print_err(f"{colors.clr('sample', Color.BOLD)} option must be followed by a number")

    # search 
    elif elems[1] == spe_args[2]:
        if nb_args < 3:
            print_err(f"{colors.clr('search', Color.BOLD)} missing argument")
        elif elems[2] not in api_resources:
            print_err(f"{colors.clr('search', Color.BOLD)} wrong ressources {colors.clr(elems[2], Color.RED)}")

def get_options(elems):
    short_opts = []
    long_opts = []

    for e in elems:
        pattern_short_opt = re.compile(r'^-\w+$')
        pattern_long_opt = re.compile(r'^--[-\w]*\w[-=\w]*$')
    
        if pattern_short_opt.match(e): 
            for chr in e[1:]:
                # print('|', chr)
                if chr.isalnum():
                    short_opts.append(chr)
        elif pattern_long_opt.match(e):
            # print(e.strip('-'))
            stripped = e.strip('-')
            if len(stripped) == 1:
                short_opts.append(stripped)
            else:
                long_opts.append(stripped) 
    
    return [short_opts, long_opts]

# DEBUG, move to test.py in unittest
def print_options(opts=user_opts):
    if opts is not None:
        for opt in opts[0]:
            print(opt)
        for opt in opts[1]:
            print(opt)

def rm_options(elems):
    return [e for e in elems if not e.startswith('-')]


def check_options(opts):
    global user_opts
    user_opts = opts

    # global opt_n

    # for opt in user_opts[1]:
    #     if opt[0] == 'n':
    #         opt_n = str(opt[2:])
    # print(user_opts)

def handle_args(elems):
    options_tmp = get_options(elems[1:])
    # print_options(options_tmp)
    args_no_opts = rm_options(elems)
    # print(args_no_opts)
    check_options(options_tmp)
    
    check_args(args_no_opts)
    if err_occured == True:
        return
    
    # print_options(options_tmp)
    
    data = switch_case(args_no_opts)
    if stream_out == True and data is not None:
        print_data(data)
        NEW_LINE()
  

##################################################################################################################################
# Main
##################################################################################################################################
    
def init():
    if stream_out == True:
        NEW_LINE()
    check_resources(verbose, stream_err)

def exit_main():
    pass

def main():
    init()
    handle_args(args)
    exit_main()
    
if __name__ == "__main__":
    main()
    
