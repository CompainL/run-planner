from flask import Blueprint, render_template, request
from website.engine.predictions import both_predictions

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/predictions', methods=['GET', 'POST'])
def predictions():
    predictions_data = None
    error = None
    distance = request.form.get('distance', '')
    time = request.form.get('time', '')
    next_goal = request.form.get('next_goal', '')

    if request.method == 'POST':
        try:
            distance_value = float(distance)
            time_value = float(time)
            target_distance = float(next_goal) if next_goal.strip() else distance_value

            if distance_value <= 0 or time_value <= 0 or target_distance <= 0:
                raise ValueError

            results = both_predictions(distance_value * 1000.0, time_value * 60.0, target_distance * 1000.0)
            predictions_data = {
                'Riegel': results['Riegel'],
                'Cameron': results['Cameron']
            }
        except ValueError:
            error = "Please enter valid positive numbers for distance, time, and goal."

    return render_template(
        "predictions.html",
        predictions=predictions_data,
        distance=distance,
        time=time,
        next_goal=next_goal,
        error=error
    )

@views.route('/make_plan')
def make_plan():
    return render_template("make_plan.html")