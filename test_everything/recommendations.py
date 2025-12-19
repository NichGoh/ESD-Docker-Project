from flask import Flask, request
from flask_cors import CORS
from invokes import invoke_http
import os
from os import environ
import requests
import pandas as pd

app = Flask(__name__)
CORS(app)

all_restaurant_url ="https://personal-wh7faulr.outsystemscloud.com/RestaurantAPI/rest/v1/AllRestaurants"
survey_URL = environ.get('survey_URL') or "http://localhost:5004/survey"


@app.route("/recommend/<string:username>", methods=['GET'])
def data(username):
    restaurant_details = invoke_http(all_restaurant_url, method='GET')
    restaurants = restaurant_details["Restaurant"]
    reco_parameters = invoke_http(survey_URL + "/" + username, method='GET')
    if reco_parameters["code"] == 404:
        return {
            "code": 404,
            "data": {
                "reco_restaurant": [],
                "all_restaurant": restaurants
            },
            "message": "No preferences data returned, no recommendations returned"
        }
    
    for restaurant in restaurants:
        if "score" in restaurant.keys():
            restaurant["score"] = 0
        else:
            temp_score = 0
            if reco_parameters["data"]["pref_cuisine"] == restaurant["Cuisine"]:
                temp_score+=1
            if reco_parameters["data"]["pref_location"] == restaurant["Location"]:
                temp_score+=1
            if reco_parameters["data"]["pref_price"] == restaurant["price_level"]:
                temp_score+=1
            restaurant["score"] = temp_score
    restaurants = sorted(restaurants, key=lambda x: x["score"],reverse=True)
    try:
        reco_restaurants = restaurants[0:5]
    except KeyError:
        pass
    return {
            "code": 201,
            "data": {
                "reco_restaurant": reco_restaurants,
                "all_restaurant": restaurants
            },
            "message": "Preferences data returned, recommendations returned"
        }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for displaying analytics...")
    app.run(host="0.0.0.0", port=5101, debug=True)