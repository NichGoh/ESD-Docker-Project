import os
from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/survey_record'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class SurveyRecord(db.Model):
    __tablename__ = 'survey_record'

    username = db.Column(db.String(60), primary_key=True)
    pref_location = db.Column(db.String(60), nullable=False)
    pref_cuisine = db.Column(db.String(60), nullable=False)
    pref_price = db.Column(db.Integer, nullable=False)

    def __init__(self, username, pref_location, pref_cuisine, pref_price):
        self.username = username
        self.pref_location = pref_location
        self.pref_cuisine = pref_cuisine
        self.pref_price = pref_price

    def json(self):
        return {"username":self.username, "pref_location":self.pref_location, "pref_cuisine":self.pref_cuisine, "pref_price":self.pref_price}
    

@app.route("/survey")
def get_all():
    surveylist = db.session.scalars(db.select(SurveyRecord)).all()
    if len(surveylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Survey": [survey.json() for survey in surveylist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no survey results."
        }
    ), 404


@app.route("/survey/<string:username>")
def find_by_survey_id(username):
    survey = db.session.scalars(db.select(SurveyRecord).filter_by(username=username).limit(1)).first()
    if survey:
        return jsonify(
            {
                "code": 200,
                "data": survey.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "username": username
            },
            "message": "User survey result not found"
        }
    ), 404

@app.route("/survey", methods=['POST'])
def create_survey_result():
    username = request.json.get('username')
    pref_location = request.json.get('pref_location')
    pref_cuisine = request.json.get('pref_cuisine')
    pref_price = request.json.get('pref_price')
    survey = SurveyRecord(username=username, pref_location=pref_location, pref_cuisine=pref_cuisine, pref_price=pref_price)

    try:
        db.session.add(survey)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the survey record. " + str(e)
            }
        ), 500
    
    print(json.dumps(survey.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": survey.json()
        }
    ), 201

@app.route("/survey/<string:username>", methods=['PUT'])
def update_survey_result(username):
    try:
        survey = db.session.scalars(db.select(SurveyRecord).filter_by(username=username).limit(1)).first()
        if not survey:
            return False

        # update status
        data = request.get_json()
        survey.pref_location = data['pref_location']
        survey.pref_cuisine = data['pref_cuisine']
        survey.pref_price = data['pref_price']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": survey.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "username": username
                },
                "message": "An error occurred while updating the survey results. " + str(e)
            }
        ), 500

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage survey results ...")
    app.run(host='0.0.0.0', port=5004, debug=True)