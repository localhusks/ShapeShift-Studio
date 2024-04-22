from urllib import response
from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from App.controllers.routine import create_routine
from App.models import db
from App.controllers import create_user,get_all_exercises,get_routine,get_routine_by_name,add_exercise_to_routine
from App.controllers.exercise import (create_exercise,get_exercise)
import requests
import json


from App.models import User
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
    exes = get_all_exercises()
    return render_template(
        'index.html',
        exercises = exes
    )



@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    user = create_user('bob', 'bobpass')
    create_routine("bob's workout",user.id)
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


@index_views.route("/routine/<int:exercise_id>", methods=['POST'])
@jwt_required()
def add_exercise(exercise_id):
    exercise = get_exercise(exercise_id)
    routine = get_routine_by_name("bob's routine")
    add_exercise_to_routine(
            exercise_id=exercise.exercise_id,
            routine_id=routine.routine_id
        )
    
    flash(f"Exercise added!")
    return redirect(request.referrer)

