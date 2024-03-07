
##################################################################################################################################
# Tools
##################################################################################################################################

from bs4 import BeautifulSoup


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

def if_none(val, new_val, empty=True):
    if empty == True and val == '':
        return new_val
    return val if val != None else new_val

def sort_tuple(tup):
    return tuple(sorted(tup))

def pretty_tuple(tup):
    output = ', '.join(str(item) for item in tup)
    return output

def clean_str(str):
    return str.replace('\t', '').replace('\n', '').replace('\r', '')

def strip_tags(html_str):
    # Use BeautifulSoup to parse and extract text without tags
    soup = BeautifulSoup(html_str, 'html.parser')
    return soup.get_text()