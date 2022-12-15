#HCDE 310 final project - Arshita Misra

import urllib.request, urllib.error, urllib.parse, json

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

def yelp_biz_det(b_id = 'cafe-solstice-seattle'):
    """Adding the business detail endpoint and generating a url"""
    url = baseurl + '/businesses/' + b_id
    biz = yelp_rest(url)
    return bizbiz(biz)


def yelp_biz_search(location = 'seattle', limit = 20):
    """Adding the business search endpoint and generating a url"""
    fullparams={'location': location, 'limit': limit}
    url = baseurl + '/businesses/' + 'search?' + urllib.parse.urlencode(fullparams)
    biz = yelp_rest(url)
    return bizbiz(biz)

def yelp_biz_rev(b_id = 'thai-tom-seattle'):
    """Adding the business reviews endpoint and generating a url"""
    url = baseurl + '/businesses/' + b_id + '/reviews'
    return yelp_rest(url)

def bizbiz(biz):
    if biz is not None:
        bdata = (json.load(biz))
        #print(pretty(bdata))
        return bdata
    return None

from math import radians, sin, cos, acos

def close_enough(user_loc, biz, radius):
    usr_lat = user_loc[0]
    usr_lon = user_loc[1]
    biz_lat=biz["coordinates"]["latitude"]
    biz_lon=biz["coordinates"]["longitude"]
    # for key in dcat:
    #     biz_lat = dcat[key]["coordinates"]["latitude"]
    #     biz_lon = dcat[key]["coordinates"]["longitude"]

    slat = radians(float(usr_lat))
    slon = radians(float(usr_lon))
    elat = radians(float(biz_lat))
    elon = radians(float(biz_lon))

    dist = 3956 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    biz['distance'] = round(dist, 2)
    if dist <= float(radius):
        return True
    return False

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('project.html',page_title="Where to go in Seattle?")

@app.route("/output")
def main_handler2():
    app.logger.info("In MainHandler")
    #loc = request.headers['X-Forwarded-For']
    category = request.args.getlist("occassion")
    open_pref = request.args.getlist("open_now")

    dcat = {}
    if 'Coffee and tea time' in category:
        fcof = open('/home/arshitamisra/mysite/list-coffee_tea.csv','r', encoding='utf-8-sig')
        flines = fcof.readlines()
        fcof.close()
        dcat['Coffee and tea time'] = flines
    if 'Fun day out' in category:
        app.logger.info("here")
        fcof = open('/home/arshitamisra/mysite/list-fun_days.csv','r', encoding='utf-8-sig')
        flines = fcof.readlines()
        fcof.close()
        dcat['Fun day out'] = flines
    if 'Dessert time!' in category:
        fcof = open('/home/arshitamisra/mysite/list-desserts.csv','r', encoding='utf-8-sig')
        flines = fcof.readlines()
        fcof.close()
        dcat['Dessert time!'] = flines
    if 'Time to party!' in category:
        fcof = open('/home/arshitamisra/mysite/list-partynight.csv','r', encoding='utf-8-sig')
        flines = fcof.readlines()
        fcof.close()
        dcat['Time to party!'] = flines
    if 'Serene study spaces' in category:
        fcof = open('/home/arshitamisra/mysite/list-studyspaces.csv','r', encoding='utf-8-sig')
        flines = fcof.readlines()
        fcof.close()
        dcat['Serene study spaces'] = flines
    if 'Eat food from around the world!' in category:
        fcof = open('/home/arshitamisra/mysite/list-around_the_world_food.csv','r', encoding='utf-8-sig')
        flines = fcof.readlines()
        fcof.close()
        dcat['Eat food from around the world!'] = flines

    for key in dcat:
        dcat[key] = [yelp_biz_det(i) for i in dcat[key]]

    if len(open_pref) > 0:
        for key in dcat:
                dcat[key] = [biz for biz in dcat[key] if biz is not None and biz.get("hours",[{"is_open_now":False}])[0]["is_open_now"]]

    ## location checking
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    radius = request.args.get("radius",10)
    if lat or lng != "":
        usr_lat = float(request.args.get('lat'))
        usr_lon = float(request.args.get('lng'))
        loc = [usr_lat,usr_lon]

        for key in dcat:
            dcat[key] = [biz for biz in dcat[key] if biz is not None and close_enough(user_loc=loc,biz=biz, radius=radius)]

    return render_template('output.html', dcat=dcat, page_title = 'Where to go?')