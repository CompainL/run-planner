from flask import Blueprint, render_template

views  = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/predictions')
def predictions():
    return render_template("predictions.html")

@views.route('/make_plan')
def make_plan():
    return render_template("make_plan.html")