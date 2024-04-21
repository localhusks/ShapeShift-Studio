from urllib import response
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user
from App.controllers.exercise import (create_exercise)
import requests

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
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
        querystring = {"limit": "20"}
        response = requests.get(url, headers=headers, params=querystring)




    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')

    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})


