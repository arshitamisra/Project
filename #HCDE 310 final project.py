#HCDE 310 final project

import urllib.request, urllib.error, urllib.parse, json, webbrowser

API_KEY = 'ovoBvyNVE8NIXzfKY2PR1QQ92jJLY6B-JJo8e2nOmGAe-Pmzjf_18VB0Tx_Q0PGohzEXuflbNxbcF2KmLOZtCJo6dZwixCs62wvgeBA1ZWd4DWVXsSbwt3t6WKt-Y3Yx'

# Utility functions
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request." )
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


baseurl = 'https://api.yelp.com/v3'
# Accessing the API
def yelp_rest(baseurl = 'https://api.yelp.com/v3', printurl=False):
    """Generating a general url to access the API without any endpoints."""
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    req = urllib.request.Request(baseurl,headers=headers)
    if printurl:
        print(req)
    result = safe_get(req)
    return result
    
yelp_rest()

def yelp_biz_det(b_id = 'french-restaurant-seattle'):
    """Adding the business detail endpoint and generating a url"""
    url = baseurl + '/businesses/' + b_id 
    return yelp_rest(url)


def yelp_biz_search():
    """Adding the business search endpoint and generating a url"""
    url = baseurl + '/businesses/' + 'search'
    return yelp_rest(url)

def yelp_biz_rev(b_id = 'french-restaurant-seattle'):
    """Adding the business reviews endpoint and generating a url"""
    url = baseurl + '/businesses/' + b_id + '/reviews'
    return yelp_rest(url)

def get_biz():
    biz = yelp_biz_det()
    if biz is not None:
        whatev = json.load(biz)
        return (pretty(whatev))
    return None

#print(get_biz())