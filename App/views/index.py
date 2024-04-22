from urllib import response
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user
from App.controllers.exercise import (create_exercise)
import requests

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
    keys_to_extract = ['bodyPart', 'equipment', 'name', 'target']
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
    base_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/"
    body_parts = [
        "back", "cardio", "chest", "lower arms", "lower legs",
        "neck", "shoulders", "upper arms", "upper legs", "waist"
    ]
    headers = {
        "X-RapidAPI-Key": "47e884c7f2msh0b51f7d588382d1p1de9dajsn5547acf5ba79",
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    querystring = {"limit":"10"}

    for part in body_parts:
        url = base_url + part
        response = requests.get(url, headers=headers, params=querystring)
        exercises_data = response.json()
        extracted_data = extract_elements(exercises_data)
        for exercise in extracted_data:
            create_exercise(
                name=exercise['name'],
                target_muscle= exercise['target'], 
                bodyPart=exercise['bodyPart'], 
                equipment=exercise['equipment']
                )
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})


