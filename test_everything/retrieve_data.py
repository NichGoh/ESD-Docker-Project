from flask import Flask, request
from flask_cors import CORS
from invokes import invoke_http
import os
import requests
from os import environ

app = Flask(__name__)
CORS(app)

restaurant_URL ="https://personal-wh7faulr.outsystemscloud.com/RestaurantAPI/rest/v1/Restaurant/"
reservation_URL = environ.get('reservation_URL') or "http://localhost:5000/reservation"

@app.route("/data", methods=['GET'])
def data():
    #invoke restaurant microservice to get place_id
    username = request.get_json()
    username = username["restaurant_username"]
    error_message1 =""
    error_message2 = ""
    error_message3 = ""
    restaurant_details = invoke_http(restaurant_URL + username + "/", method='GET')
    if "code" in restaurant_details:
        error_message1="No restaurant data available"
    else:
        restaurant_placeid = restaurant_details["Restaurant"]["place_id"]
        error_message1 = "Successful restaurant data request"

    #call google api for google reviews real time
    reviews_call = requests.get("https://maps.googleapis.com/maps/api/place/details/json?place_id="+ restaurant_placeid + "&fields=reviews,rating,user_ratings_total&key=") #Enter your google api key here
    if (reviews_call.json()["status"]== 'INVALID_REQUEST'):
        review = []
        error_message2 = "Invalid request to Google Apis"
    else:
        review = reviews_call.json()["result"]
        error_message2 = "Google Apis request success"

    #invoke reservation microservice
    reservation = invoke_http(reservation_URL + "/" + username, method='GET')
    if reservation["code"]!= 404:
        reservation = reservation["data"]
        error_message3 = "Successful reservation request"
    else:
        reservation =[]
        error_message3 = "Invalid reservation request"

    if error_message1 == "No restaurant data available" or error_message2 == "Invalid request to Google Apis" or error_message3 == "Invalid reservation request":
        return{
            "code": 500,
            "data": {
                "review": review,
                "reservation": reservation
            },
            "messages": {"Restaurant_API" :error_message1,"Google_API":error_message2,"Reservation_API":error_message3}
        } 
    else:
        return {
            "code": 201,
            "data": {
                "review": review,
                "reservation": reservation
            },
            "messages": "Request success"
        }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for displaying analytics...")
    app.run(host="0.0.0.0", port=5003, debug=True)

        
