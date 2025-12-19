import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from os import environ
from datetime import datetime
import json
import string
import random
import requests
# from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# load_dotenv()

# Authentication_API = os.getenv('AUTHENTICATION_API')
app = Flask(__name__)

Authentication_API = environ.get("authentication_URL") or 'http://localhost:4000/'

@app.route('/get-data', methods=['GET'])
@cross_origin()
def get_data():
    # Your logic to process the GET request goes here
    # For now, let's return a sample response
    return jsonify({'message': 'GET request received successfully!'})

@app.route('/testadd', methods=['POST'])
@cross_origin()
def testadd():
    try:
        data = request.get_json()
        userData = data['userData']
        resturantData = data['resturantData']
        
        print(resturantData)
        # get_user_token = requests.post(Authentication_API+'users/login', json={'Username': userData['Username'], 'Password': userData['Password']})
        # get_user_token.raise_for_status()
        # get_user_token = get_user_token.json()
        # if token key is not in the response, return the response
        # if 'token' in get_user_token:
        #     return get_user_token, 200
        # if token key is in the response, continue with the process
        return jsonify({resturantData}), 200

    except requests.exceptions.RequestException as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400



@app.route('/addRestaurant', methods=['POST'])
@cross_origin()
def addRestaurent():
    try:
        data = request.get_json()
        userData = data['userData']
        resturantData = data['resturantData']
        # create user 
        create_user = requests.post(Authentication_API+'users/register', json=userData)
        create_user.raise_for_status()
        # Make a request to find the place ID
        place_id_params = {
            'inputtype': 'textquery',
            'input': resturantData['Name'],
            'key': ''  # Replace with your actual API key
        }
        place_id_response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', params=place_id_params)
        place_id_response.raise_for_status()
        place_id_data = place_id_response.json()
        place_id = place_id_data['candidates'][0]['place_id']
        
        # Make a request to get the price level
        price_level_params = {
            'place_id': place_id,
            'fields': 'price_level',
            'key': 'AIzaSyD0D0t9ZTt1MYbn71HbNYj59BS6RbgW8VQ'  # Replace with your actual API key
        }
        print(price_level_params)
        price_level_response = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params=price_level_params)
        price_level_response.raise_for_status()
        price_level_data = price_level_response.json()
        print(price_level_response)
        # price_level_data['result']['price_level'] if exist
        if 'result' in price_level_data and 'price_level' in price_level_data['result']:
            price_level = price_level_data['result']['price_level']
        else:
            price_level = 0

        # post to outsystem
        restuarantPost = {
            'username': userData['Username'],
            'email': userData['Email'],
            'Name': resturantData['Name'],
            'Opening_hours': resturantData['Opening_hours'],
            'Location': resturantData['Location'],
            'Cuisine': resturantData['Cuisine'],
            'Contact': resturantData['Contact'],
            'Title_image': resturantData['Title_image'],
            'price_level': price_level,
            'place_id': place_id
        }
        resturantOutsystem = requests.post('https://personal-wh7faulr.outsystemscloud.com/RestaurantAPI/rest/v1/AddRestaurants/', json=restuarantPost)
        
        resturantOutsystem.raise_for_status()
        # test
        # resturantOutsystem = requests.get('https://personal-wh7faulr.outsystemscloud.com/RestaurantAPI/rest/v1/Restaurant/test12345test12345test12345test12345123asd/')
        
        # get user token
        get_user_token = create_user.json()
        # if token key is not in the response, return the response
        if 'token' in get_user_token:
            return get_user_token, 201
        # if token key is in the response, continue with the process
        

    except requests.exceptions.RequestException as e:
        print(e)
        return jsonify({'error': str(e),  "code":500}), 500

    except Exception as e:
        print(e)
        return jsonify({'error': str(e),  "code":400}), 400

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": Mange user creation ...")
    app.run(host='0.0.0.0', port=4001, debug=True)