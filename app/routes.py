
from app import app
import requests, json

from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_user, logout_user

from .auth.forms import SignUpForm, LoginForm
from .models import User

@app.route('/')
def homePage():
    return render_template('index.html')






