#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime
import json
import string
import random

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/loyalty_record'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/loyalty_record'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class LoyaltyPoints(db.Model):
    # __tablename__ = 'loyaltypoints'
    __tablename__ = 'loyalty_record'

    # user_id = db.Column(db.Integer, primary_key=True)
    # loyalty_points = db.Column(db.String(3), nullable=False)
    username = db.Column(db.String(60), primary_key=True)
    loyalty_points = db.Column(db.Integer, nullable=False)

    def __init__(self, username, loyalty_points):
        self.username = username
        self.loyalty_points = loyalty_points

    def json(self):
        return {"username":self.username, "loyalty_points": self.loyalty_points }

class VoucherCodes(db.Model):
    __tablename__ = 'voucher_codes'

    voucher_code = db.Column(db.String(10), primary_key=True)

    def __init__(self, voucher_code):
        self.voucher_code = voucher_code

    def json(self):
        return {"voucher_code":self.voucher_code}    


@app.route("/loyalty_record")
def getAllPoints():
    #get whole db
    pointslist = db.session.scalars(db.select(LoyaltyPoints)).all()
    if len(pointslist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "points": [points.json() for points in pointslist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404

@app.route("/loyalty_record/<string:username>")
def getPoints(username):
    #get points of specific user from db, should come back as json type {userid, number of points}
    points = db.session.scalars(db.select(LoyaltyPoints).filter_by(username=username).limit(1)).first()
    if points:
        return jsonify(
            {
                "code": 200,
                "data": points.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "username": username
            },
            "message": "User not found."
        }
    ), 404

@app.route("/loyalty_record/<string:username>",methods=["POST"])
def updatePoints(username):
    #access the User Database
    if not(db.session.scalars(db.select(LoyaltyPoints).filter_by(username=username).limit(1)).first()):
        user = LoyaltyPoints(username, 1)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "username": username
                    },
                    "message": "An error occurred creating the user."
                }   
            ), 500
        return jsonify(
            {
                "code": 201,
                "data": user.json()
            }
        ), 201
    try:
        data = request.get_json()
        loyalty_points = data['loyalty_points']
        points = db.session.scalars(db.select(LoyaltyPoints).filter_by(username=username).limit(1)).first()
        # update status
        points.loyalty_points += int(loyalty_points)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": points.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "username": username
                },
                "message": "User not found"
            }
        ), 500
    
@app.route("/loyalty_record/<string:username>",methods=["PUT"])
def generateCode(username):
    pointsjson = db.session.scalars(db.select(LoyaltyPoints).filter_by(username=username).limit(1)).first()
    print(pointsjson.loyalty_points)
    points = pointsjson.loyalty_points
    if points>=5:
        try:
            pointsjson.loyalty_points -= 5
            db.session.commit()
        except:
            print('error')
        characters = string.ascii_uppercase + string.digits
        voucher_code=''
        for x in range(10):
            # voucher_code = 'AAAAAAAAAA'
            voucher_code += random.choice(characters)
        if not (db.session.scalars(db.select(VoucherCodes).filter_by(voucher_code=voucher_code).limit(1)).first()):
            voucher = VoucherCodes(voucher_code)
            try:
                points = points - 5
                db.session.add(voucher)
                db.session.commit()
            except:
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "voucher_code": voucher_code
                        },
                        "message": "An error occurred creating the voucher."
                    }   
                ), 500
            return jsonify(
                {
                    "code": 201,
                    "data": {
                        "voucher_code":voucher_code
                    },
                    "message": "Voucher created"
                }
            ), 201
        else:
            print('Voucher already exists')
            repeated = True
            while repeated:
                voucher_code=''
                for x in range(10):
                    voucher_code += random.choice(characters)
                if not (db.session.scalars(db.select(VoucherCodes).filter_by(voucher_code=voucher_code).limit(1)).first()):
                    repeated = False
            voucher = VoucherCodes(voucher_code)
            try:
                db.session.add(voucher)
                db.session.commit()
            except:
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "voucher_code": voucher_code
                        },
                        "message": "An error occurred creating the voucher."
                    }   
                ), 500
            return jsonify(
                {
                    "code": 201,
                    "data": {
                        "voucher_code":voucher_code
                    },
                    "message": "Voucher created"
                }
            ), 201
    else:
        return jsonify(
                {
                    "code": 400,
                    "data": {
                        "points":points
                    },
                    "message": "User not enough points"
                }
            ), 400
            
        

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5001, debug=True)