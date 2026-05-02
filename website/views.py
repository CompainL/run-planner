from flask import Blueprint, render_template, request
from website.engine.predictions import both_predictions
from website.engine.session_planner import Session

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

@views.route('/make_plan', methods=['GET', 'POST'])
def make_plan():
    session = None
    error = None

    if request.method == 'POST':
        try:
            session_name = request.form.get('session_name', '')
            cycle_rate = float(request.form.get('cycle_rate', 0))
            cycle_duration = float(request.form.get('cycle_duration', 0))
            number_of_cycles = int(request.form.get('number_of_cycles', 0))
            run_speed_target = request.form.get('run_speed_target', '')
            walk_speed_target = request.form.get('walk_speed_target', '')
            distance_target = request.form.get('distance_target', '')

            if cycle_rate <= 0 or cycle_duration <= 0 or number_of_cycles <= 0:
                raise ValueError


            session = Session(
                cycle_rate=cycle_rate,
                cycle_duration=cycle_duration,
                number_of_cycles=number_of_cycles,
                session_name=session_name,
                run_speed_target=float(run_speed_target) if run_speed_target else None,
                walk_speed_target=float(walk_speed_target) if walk_speed_target else None,
                distance_target=float(distance_target) if distance_target else None
            )
        except ValueError:
            error = "Please enter valid positive numbers for all fields."

    return render_template(
        "make_plan.html",
        session=session,
        error=error
    )