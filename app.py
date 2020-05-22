# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# weather webhook apiai
from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    # commented out by Naresh
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    print ("starting processRequest...")
    if req.get("queryResult").get("action") != "yahooWeatherForecast":
        return {}
    #baseurl = "https://query.yahooapis.com/v1/public/yql?"
    #yql_query = makeYqlQuery(req)
   # if yql_query is None:
       # return {}
    yql_url = "https://api.thingspeak.com/channels/107478/feeds.json?results=1"
    result = urlopen(yql_url).read()
    #data = json.loads(result)
    #for some the line above gives an error and hence decoding to utf-8 might help
    data = json.loads(result.decode('utf-8'))
    res = makeWebhookResult(data)
    #zap_url="https://hooks.zapier.com/hooks/catch/3174192/fdhs6r?dataq="+res
    #result1 = urlopen(zap_url).read()
    #zapactivate=json.loads(result1)
    print ("zap activated zooooop!!")
    #print (zapactivate)
    return res


"""def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None
    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"/"""


def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    feeds = data.get('feeds')[0]
    if feeds is None:
        return {}
    #for r in feeds:
        #return r["field1"]
    field1 = feeds.get('field1')
    if field1 is None:
        return {}

    

    
      

    # print(json.dumps(item, indent=4))

    speech = "Today the water level of main tank is " + feeds.get('field1')
    print("Response:")
    print(speech)
    return speech


@app.route('/test', methods=['GET'])
def test():
    app = ClarifaiApp(api_key='d1c9df3c907e48e1a317856eea26c099')
    model = app.public_models.general_model
    model.model_version = 'aa7f35c01e0642fda5cf400f543e7c40'
    response = model.predict([ClImage(url="https://drive.google.com/uc?id=1r4gH7zDmQ24cuB-26PgLuyb7ncU_2WMY&export=download")])
    print(response)
    
    return "Done"

@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    my_result =  {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')







"""from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    # commented out by Naresh
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    print ("starting processRequest...",req.get("queryResult").get("action"))
    if req.get("queryResult").get("action") == "NOTyahooWeatherForecasT":
        return {}
    yql_url = "https://api.thingspeak.com/channels/107478/feeds.json?results=1"
    print(req)
  
    result = urlopen(yql_url).read()
    #data = json.loads(result)
    #for some the line above gives an error and hence decoding to utf-8 might help
    data = json.loads(result.decode('utf-8'))
    res = makeWebhookResult(data)
    return res



def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    feeds = data.get('feeds')
    if feeds is None:
        return {}

    field1 = feeds.get('field1')
    if field1 is None:
        return {}

    

    
      

    # print(json.dumps(item, indent=4))

    speech = "Today the water level of main tank is " + feeds.get('field1')
    print("Response:")
    print(speech)

    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
         {
          "text": [
           "text response"
          ],
         }
        ],
          # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


@app.route('/test', methods=['GET'])
def test():
    return  "Hello there my friend !!"


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    my_result =  {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')


#*************************************************************************************************************************"""

