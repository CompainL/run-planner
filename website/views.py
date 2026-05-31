import json
import re
from datetime import datetime
from pathlib import Path

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

def _get_session_dir():
    session_dir = Path(__file__).resolve().parent / 'data' / 'sessions'
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def _sanitize_filename(session_name: str) -> str:
    safe_name = re.sub(r'[^A-Za-z0-9_-]+', '_', (session_name or 'session').strip())
    return safe_name.strip('_') or 'session'


def _save_session_json(session_obj: Session) -> str:
    session_dir = _get_session_dir()
    filename = f"{_sanitize_filename(session_obj.name)}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    file_path = session_dir / filename
    with file_path.open('w', encoding='utf-8') as file:
        json.dump(session_obj.to_dict(), file, indent=2)
    return filename


def _load_session_json(filename: str) -> Session:
    session_dir = _get_session_dir()
    file_path = session_dir / filename
    with file_path.open('r', encoding='utf-8') as file:
        data = json.load(file)
    return Session.from_dict(data)


def _list_saved_sessions():
    session_dir = _get_session_dir()
    sessions = []
    for file_path in sorted(session_dir.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(file_path.read_text(encoding='utf-8'))
            sessions.append({
                'filename': file_path.name,
                'name': data.get('name', 'Unnamed Session'),
                'cycle': data.get('cycle', {}),
                'created_at': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
        except (json.JSONDecodeError, OSError):
            continue
    return sessions


@views.route('/make_session', methods=['GET', 'POST'])
def make_session():
    session = None
    error = None
    saved = False
    saved_filename = None
    saved_sessions = _list_saved_sessions()

    if request.method == 'POST':
        try:
            submit_action = request.form.get('submit_action', 'simulate')

            if submit_action == 'load':
                filename = request.form.get('filename', '')
                if not filename:
                    raise ValueError
                session_obj = _load_session_json(filename)
            else:
                session_name = request.form.get('session_name', '').strip() or 'Demo Session'
                cycle_rate = float(request.form.get('cycle_rate', 0))
                cycle_duration = float(request.form.get('cycle_duration', 0))
                number_of_cycles = int(request.form.get('number_of_cycles', 0))
                run_speed_target = request.form.get('run_speed_target', '')
                walk_speed_target = request.form.get('walk_speed_target', '')
                distance_target = request.form.get('distance_target', '')

                if cycle_rate <= 0 or cycle_duration <= 0 or number_of_cycles <= 0:
                    raise ValueError

                session_obj = Session(
                    cycle_rate=cycle_rate,
                    cycle_duration=cycle_duration,
                    number_of_cycles=number_of_cycles,
                    session_name=session_name,
                    run_speed_target=float(run_speed_target) if run_speed_target else None,
                    walk_speed_target=float(walk_speed_target) if walk_speed_target else None,
                    distance_target=float(distance_target) if distance_target else None
                )
                if submit_action == 'save':
                    saved_filename = _save_session_json(session_obj)
                    saved = True
                    saved_sessions = _list_saved_sessions()

            session = session_obj.to_dict()
        except (ValueError, FileNotFoundError, json.JSONDecodeError):
            error = "Please enter valid positive numbers for all fields, or load a valid saved session."

    return render_template(
        "add_session.html",
        session=session,
        error=error,
        saved=saved,
        saved_filename=saved_filename,
        saved_sessions=saved_sessions
    )