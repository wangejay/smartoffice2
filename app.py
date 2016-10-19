#!/usr/bin/env python

import urllib
import json
import os
import sys

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    return res


def processRequest(req):
    #JW
    if req.get("result").get("action") != "bookmeetingroom":
        return {}
    #JW
    yql_query = makeYqlQuery(req)
    print (yql_query)
    
    print ("processRequest")

    subject_resoult = makesubjectQuery(req)
    print (subject_resoult)
    date_resoult = makedateQuery(req)
    #date_string=date_resoult[3:13]
    print (date_resoult)
    #date_string=date_resoult[3:13]
    any_string=subject_resoult
    p_comment= "python calendar_manage.py "+ "2016-10-20" +" "+"heroku"
    os.system(p_comment)
    return "booking"



def makedateQuery(req):
    print ("makedateQuery in")
    result = req.get("result")
    parameters = result.get("parameters")
    date_query = parameters.get("date")
    if date_query is None:
        return None
    return date_query

def makesubjectQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    any_query = parameters.get("any")
    if any_query is None:
        return None
    return any_query

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
