from flask import Blueprint, render_template, request, session, redirect, url_for
from ..authentication.authentication import RegistrationForm, LoginForm
from podcast.authentication.services import auth_services
from podcast.blueprints.services import *

authentication_blueprint = Blueprint(
    'authentication_bp', __name__)

@authentication_blueprint.route('/authentication/register', methods=['GET', 'POST'])
def register():
    authentication_type = "Register"
    form = RegistrationForm()
    repo_instance = get_repo()

    if form.validate_on_submit():
        if not auth_services.user_registered(form.username.data, repo_instance): # --------------------------------------
            auth_services.register_user(form.username.data, form.password.data, repo_instance) # --------------------------------------
            session.clear()
            session['username'] = form.username.data
            print(f"Registered and logged in as {form.username.data}")
            return redirect(url_for('home_bp.home'))
        else:
            print("Username already exists!")

    return render_template('authentication.html',
                           auth_type=authentication_type, form=form)


@authentication_blueprint.route('/authentication/login', methods=['GET', 'POST'])
def login():
    repo_instance = get_repo()
    authentication_type = "Login"
    form = LoginForm()

    # Checks if username exists in Memory Repository, password check is in LoginForm
    if form.validate_on_submit():
        if auth_services.user_registered(form.username.data, repo_instance): # --------------------------------------
            if auth_services.authenticate_user(form.username.data, form.password.data, repo_instance): # --------------------------------------
                session.clear()
                session['username'] = form.username.data
                return redirect(url_for('home_bp.home'))
        else:
            print("Incorrect Username or Password!")
        return redirect(url_for('authentication_bp.login'))

    return render_template('authentication.html',
                           auth_type=authentication_type, form=form)


@authentication_blueprint.route('/authentication/logout')
def logout():
    session.clear()
    users = get_users() # --------------------------------------
    print(users)
    return redirect(url_for('home_bp.home'))
