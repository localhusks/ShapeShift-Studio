from App.models import Exercise
from App.database import db

def create_exercise(name,target_muscle,bodyPart,equipment):
    try:
        exercise = Exercise(
            name=name,
            body_area=bodyPart,
            equip=equipment,
            muscle=target_muscle
        )
        db.session.add(exercise)
        db.session.commit()
        return exercise
    except Exception as e:
        print('error in creating Exercise:', e)
        db.session.rollback()
        return None
    
def get_exercise(id):
    return Exercise.query.get(id)

def get_all_exercises():
    return Exercise.query.all()

def get_all_exercises_json():
    exercises = get_all_exercises()
    return [e.to_json() for e in exercises]

def get_all_exercises_by_body_part(part):
    exercises = Exercise.query.filter_by(body_area=part).all()
    return [e.to_json() for e in exercises]

def get_all_exercises_by_target_muscle(muscle):
    exercises = Exercise.query.filter_by(target_muscle = muscle).all()
    return [e.to_json() for e in exercises]

def get_all_exercises_by_equipment(equip):
    exercises = Exercise.query.filter_by(equipment = equip).all()
    return [e.to_json() for e in exercises]

