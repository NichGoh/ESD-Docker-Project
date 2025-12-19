from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http
import logging

import pika
import json
from os import environ

# Assuming you have the create_connection function from your AMQP setup file
import amqp_connection
logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
CORS(app)

reservation_URL = environ.get('reservation_URL') or "http://localhost:5000/reservation"
loyalty_URL = environ.get('loyalty_URL') or "http://localhost:5001/loyalty_record"

connection = amqp_connection.create_connection()
channel = connection.channel()

if not amqp_connection.check_exchange(channel, 'reservation_topic', "topic"):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

@app.route("/make_reservation", methods=['POST'])
def make_reservation():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:        
            reservation = request.get_json()
            print("\nReceived a reservation in JSON:", reservation)
            # do the actual work
            
            result = processPlaceReservation(reservation)
            print(reservation)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_reservation.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400



# Function to send email confirmation via AMQP
def send_email_confirmation(reservation):
    
    # Prepare the message to be sent
    message = {
        "user_id": reservation["data"]["user_username"],
        "email":reservation["data"]["user_email"],
        "restaurant_name":reservation["data"]["restaurant_name"],
        "reservation_id": reservation["data"]["reservation_id"],
        "reservation_date": reservation["data"]["reservation_date"],
        "num_of_pax": reservation["data"]["num_of_pax"],
        "type": "reservation"
    }

    print(message)

    # Publish the message to the queue
    channel.basic_publish(exchange='reservation_topic', routing_key='email.queue', body=json.dumps(message), properties=pika.BasicProperties(delivery_mode=2))
    print("Email confirmation message sent to queue.")


def processPlaceReservation(reservation):
    
    email = reservation["user_email"]
    del reservation["user_email"]
    print('\n-----Invoking reservation microservice-----')
    reservation_result = invoke_http(reservation_URL, method='POST', json=reservation)
    print('reservation_result:', reservation_result)
    # Extract the username from the reservation data
    # username = reservation_result['username']
    username = reservation_result.get('data', {}).get('user_username')
    reservation_id = reservation_result.get('data', {}).get('reservation_id')

    # Prepare data for loyalty points microservice
    # This is just an example. Adjust the data according to your loyalty_points microservice's requirements.
    loyalty_points_data = {
        "loyalty_points": 2 # Example points to add or subtract
    }

    print('\n\n-----Invoking loyalty_points microservice-----')
    logging.info('Invoking loyalty_points microservice with URL: %s', loyalty_URL)

    loyalty_points_result = invoke_http(loyalty_URL +"/"+ username, method='POST', json=loyalty_points_data)
    print("loyalty_points_result:", loyalty_points_result, '\n')

    logging.info('Loyalty points microservice invoked successfully.')
    reservation_result['data']["user_email"] = email
    send_email_confirmation(reservation_result)


    # loyalty_points_url = f"{loyalty_URL}/{username}"

    # print('\n\n-----Invoking loyalty_points microservice-----')
    # logging.info('Invoking loyalty_points microservice with URL: %s', loyalty_points_url)

    # # Assuming invoke_http can handle the URL construction and method correctly
    # loyalty_points_result = invoke_http(loyalty_points_url, method='PUT', json=loyalty_points_data)
    # print("loyalty_points_result:", loyalty_points_result, '\n')

    # logging.info('Loyalty points microservice invoked successfully.')

    return {
        "code": 201,
        "data": {
            "reservation_result": reservation_result,
            "loyalty_points_result": loyalty_points_result
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
