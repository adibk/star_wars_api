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

# Get the arguments from command line
args = sys.argv

# URLs
url = {}
url['base'] = 'https://swapi.dev/api/'
url['planet'] = 'https://swapi.dev/api/planets/'

def get_url_search(ressource, schema):
    return 'https://swapi.dev/api/' + ressource + '/?search=' + schema

# Fetch from api string data, http request
def fetch_data(url):
    try:
        # Get request timeout of 5 seconds
        response = requests.get(url, timeout=5)
        
        # Check the status code
        response.raise_for_status()
        
        return response.text
    except requests.RequestException as e:
        # errors (e.g., connection refused, timeout exceeded, etc.)
        print(f"An HTTP request error occurred: {e}")
        return None

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


#
# Handling specific data
# Ressources from base
# Planets
# Make a seach
#

def get_ressources():
    data = fetch_data(url['base'])
    return str_to_json(data)

def ressources():
    df = get_ressources()
    
def get_planet(n):
    data = fetch_data(url['planet'] + str(n))
    return str_to_json(data)

def search(ressource, s):
    #print(get_url_search(ressource, s))
    data = fetch_data(get_url_search(ressource, s))
    return str_to_json(data)

#
# Handling arguments
#
   
def switch_case(main_args):
    case = main_args[1]
    if case == 'ressources':
        return get_ressources()
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
    handle_args(args)
    print("\n")
    ressources()
    
if __name__ == "__main__":
    main()
    
