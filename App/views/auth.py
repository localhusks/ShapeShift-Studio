from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from sqlalchemy.exc import IntegrityError
from.index import index_views
from App.controllers import login
from App.controllers import (
    create_user
)
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    current_user
)
auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


'''
Page/Action Routes
'''    
@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    
@auth_views.route('/', methods=['GET'])
@auth_views.route('/login', methods=['GET'])
def login_page():
  return render_template('login.html')

@auth_views.route('/signup', methods=['GET'])
def signup_page():
  return render_template('signup.html')

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    if token:
        flash(f"User {data['username']} logged in successfully")
        response = redirect(url_for('index_views.index_page'))
        set_access_cookies(response,token)
        return response
    flash("Invalid Username or Password")
    return redirect(url_for('login_page'))

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    flash('Logged Out')
    response = redirect(url_for('login_page'))
    unset_jwt_cookies(response)
    return response

@auth_views.route("/signup", methods=['POST'])
def signup_action():
    response = None
    try:
        data = request.form
        username = request.form['username']
        password = request.form['password']
        user = create_user(
            username=username,
            password=password
        )
        flash('Account created')
        response = redirect(url_for('index_views.index_page'))
        token = create_access_token(identity=user)
        set_access_cookies(response, token)
    except IntegrityError:
        flash('Username already exists')
        response = redirect(url_for('signup_page'))
    return response


# @auth_views.route('/app', methods=['GET'])
# @jwt_required()
# def home_page():
#     return render_template('index.html')