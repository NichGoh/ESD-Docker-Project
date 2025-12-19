from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import random
from os import environ

app = Flask(__name__)
cors = CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/reservation'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/reservation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Reservation(db.Model):
    __tablename__ = 'reservation'

    username = db.Column(db.String(60))
    restaurant_name = db.Column(db.String(60))
    
    reservation_date = db.Column(db.Date, nullable=False)
    reservation_time = db.Column(db.Time, nullable=False)
    num_of_pax = db.Column(db.Integer)
    special_requests = db.Column(db.String(60))

    reservation_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, username,restaurant_name, reservation_date, reservation_time, num_of_pax, special_requests, reservation_id):
        self.username = username
        self.restaurant_name = restaurant_name
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.num_of_pax = num_of_pax
        self.special_requests = special_requests
        self.reservation_id = reservation_id

        
    def json(self):
        
        return {"username": self.username, 
        "restaurant_name": self.restaurant_name, 
        "reservation_date": str(self.reservation_date),
        "reservation_time": str(self.reservation_time),
        "num_of_pax": self.num_of_pax,
        "special_requests": self.special_requests,
        "reservation_id": self.reservation_id}

        # return json.dumps({"username": self.username, restaurant_name": selfrestaurant_name, 
        # "num_of_pax": self.num_of_pax,
        # "special_requests": self.special_requests,
        # "reservation_id": self.reservation_id,
        # "reservation_date": self.reservation_date,
        # "reservation_time": self.reservation_time}, default=str)

        # return json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)


@app.route("/reservation")
def get_all():
    # get all reservations and all reservation details
    reservationlist = db.session.scalars(db.select(Reservation)).all()

    if len(reservationlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "reservationlist": [reservation.json() for reservation in reservationlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no reservations."
        }
    ), 404

@app.route("/reservation/<string:restaurant_name>")
def find_by_restaurant_name(restaurant_name):
    # find by restaurant_name
    reservations = db.session.scalars(
        db.select(Reservation).filter_by(restaurant_name=restaurant_name)).all()

    if reservations:
        return jsonify(
            {
                "code": 200,
                "data": [reservation.json() for reservation in reservations]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Restaurant not found."
        }
    ), 404
   

@app.route("/reservation/<int:reservation_id>")
def find_by_reservation_id(reservation_id):
# find by reservation_id
    reservation = db.session.scalars(
    db.select(Reservation).filter_by(reservation_id=reservation_id).
    limit(1)
).first()

    if reservation:
        return jsonify(
            {
                "code": 200,
                "data": reservation.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Reservation not found."
        }
    ), 404


@app.route("/reservation", methods=['POST'])
# create a reservation with all details, generates own reservation_id
def create_reservation():
    try: 
        reservation_id = random.randint(1000, 9999)
        if db.session.query(Reservation).filter_by(reservation_id=reservation_id).first():
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "reservation_id": reservation_id
                    },
                    "message": "Reservation already exists, choose another date."
                }
            ), 400



        data = request.get_json()
        data['reservation_id'] = reservation_id  
        
        reservation = Reservation(**data)

        db.session.add(reservation)
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": {
                    "username": reservation.username,
                    "reservation_id": reservation.reservation_id,
                    "restaurant_name": reservation.restaurant_name,
                    "reservation_date": str(reservation.reservation_date),
                    "reservation_time": str(reservation.reservation_time),
                    "num_of_pax": reservation.num_of_pax,
                    "special_requests": reservation.special_requests
                }
            }
        ), 201

    except IntegrityError:
        db.session.rollback()  # Rollback transaction in case of IntegrityError
        return jsonify({
            "code": 500,
            "message": "An error occurred while processing the request. Please try again later."
        }), 500

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
