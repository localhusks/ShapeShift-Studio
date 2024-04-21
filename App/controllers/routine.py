from App.models import Routine
from App.database import db
from App.models import Exercise

def create_routine(name, user_id):
    try:
        newroutine = Routine(
            name = name,
            user_id = user_id
        )
        db.session.add(newroutine)
        db.session.commit()
        return newroutine
    except Exception as e:
        print(f'error in creating routine for user: {user_id}', e)
        db.session.rollback()
        return None
    
def get_routine(id):
    return Routine.query.get(id)

def get_routine_by_name(name):
    return Routine.query.filter_by(custom_name = name).first()

def get_all_routines_for_user(user_id):
    return Routine.query.filter_by(user_id =user_id).all()

def get_all_routines_for_user_json(user_id):
    routines = get_all_routines_for_user(user_id)
    return [r.to_json() for r in routines]

def delete_routine(id):
    try:
        routine = get_routine(id)
        db.session.delete(routine)
        db.session.commit()
        return True
    except Exception as e:
        print('error in deleting routine for user', e)
        db.session.rollback()
        return False

