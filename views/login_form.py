import os

from flask import render_template, flash, redirect, request, url_for

from flask_login import current_user, login_user, logout_user
from models.user import User

from app import app
from controllers.user_controller import UserController
from forms.forms import LoginForm

TITLE = "Login"
controller = UserController()


@app.route("/login", methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    return render_template('login.html', form=form, title=TITLE)


@app.route("/login", methods=['POST'])
def login_post():
    login_form = LoginForm(request.form)
    username = request.form["username"]
    password = request.form["password"]

    user = controller.autenticate_user(username, password)
    if user is not None:
        #todo:Remember me
        login_user(user)
        return redirect("/")
    else:
        flash('Invalid username or password')
        return redirect("login")


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")
