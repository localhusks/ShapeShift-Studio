from urllib import response
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user
from App.controllers.exercise import (create_exercise)
import requests
import json
index_views = Blueprint('index_views', __name__, template_folder='../templates')
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    current_user
)
def extract_elements(data):
    keys_to_extract = ['difficulty', 'equipment', 'name', 'target']
    extracted_elements = [{key: exercise[key] for key in keys_to_extract} for exercise in data]
    return extracted_elements

@index_views.route('/app', methods=['GET'])
@jwt_required()
def index_page():
    return render_template('index.html')



@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    base_url = "https://api.api-ninjas.com/v1/exercises"
    headers={'X-Api-Key': 'p7qwwiLPwaRqMsHglv/zOA==IHNYDMBP2qd3rItm'}
    

    url = base_url
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.ok:
        exercises_data = json.loads(response.text)
    for exercise_data in exercises_data:

        name = exercise_data["name"]
        difficulty = exercise_data["difficulty"]
        muscle = exercise_data["muscle"]
        equipment = exercise_data["equipment"]

        try:
            exercise = create_exercise(name, muscle, difficulty, equipment)
            if exercise:
                print(f"Exercise '{name}' created successfully.")
            else:
                print(f"Failed to create exercise '{name}'.")
        except Exception as e:
            print('Error in creating Exercise:', e)

    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})


