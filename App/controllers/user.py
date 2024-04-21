from App.models import User
from App.models import Routine
from App.database import db

def create_user(username, password):
    try:
        newuser = User(
            username=username, 
            password=password,
            )
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except Exception as e:
        print('error in creating user: ', e)
        db.session.rollback()
        return None

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.to_json() for user in users]
    return users

def update_user(id, username):
    try:
        user = get_user(id)
        if user:
            user.set_username(username)
            db.session.add(user)
            db.session.commit()
            return user
    # return None
    except Exception as e:
        print('error in updating username: ', e)
        db.session.rollback()
        return None
    
def add_routine_to_user(id,routine):
    try:
        user = get_user(id)
        if user:
            user.add_routine(routine)
            db.session.add(user)
            db.session.commit()
            return user
    # return None
    except Exception as e:
        print('error in adding routine to user: ', e)
        db.session.rollback()
        return None
    
def remove_routine_from_user(id,routine):
    try:
        user = get_user(id)
        if user:
            user.remove_routine(routine)
            db.session.add(user)
            db.session.commit()
            return user
    # return None
    except Exception as e:
        print('error in removing routine from user: ', e)
        db.session.rollback()
        return None