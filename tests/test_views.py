import json
from website import create_app
from website import views as views_module


def test_home_page_renders():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.get('/')

    assert response.status_code == 200
    assert b'Welcome to the Run Planner' in response.data
    assert b'Your one-stop solution for planning your runs efficiently.' in response.data


def test_make_plan_page_renders():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.get('/make_plan')

    assert response.status_code == 200
    assert b'Create Your Run Plan' in response.data


def test_predictions_post_valid_input_shows_results():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/predictions',
            data={
                'distance': '5',
                'time': '25',
                'next_goal': '10',
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Run Predictions' in response.data
    assert b'Riegel Prediction' in response.data
    assert b'Cameron Prediction' in response.data
    assert b'Expected time' in response.data


def test_predictions_post_invalid_input_shows_error():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/predictions',
            data={
                'distance': '-1',
                'time': '0',
                'next_goal': '10',
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Please enter valid positive numbers for distance, time, and goal.' in response.data


def test_predictions_post_blank_next_goal_uses_distance():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/predictions',
            data={
                'distance': '5',
                'time': '25',
                'next_goal': '',
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Run Predictions' in response.data
    assert b'Riegel Prediction' in response.data
    assert b'Cameron Prediction' in response.data


def test_make_plan_post_valid_input_shows_session_summary():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/make_plan',
            data={
                'session_name': 'Morning Run',
                'cycle_rate': '60',
                'cycle_duration': '8',
                'number_of_cycles': '4',
                'run_speed_target': '10',
                'walk_speed_target': '5',
                'distance_target': '8',
                'submit_action': 'simulate',
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Morning Run' in response.data
    assert b'Run time:' in response.data
    assert b'Walk time:' in response.data


def test_make_plan_post_save_session_creates_json_file(tmp_path, monkeypatch):
    monkeypatch.setattr(views_module, '_get_session_dir', lambda: tmp_path)

    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/make_plan',
            data={
                'session_name': 'Saved Run',
                'cycle_rate': '70',
                'cycle_duration': '10',
                'number_of_cycles': '3',
                'run_speed_target': '12',
                'walk_speed_target': '6',
                'distance_target': '10',
                'submit_action': 'save',
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Session saved as' in response.data

    saved_files = list(tmp_path.glob('*.json'))
    assert len(saved_files) == 1

    saved_data = json.loads(saved_files[0].read_text(encoding='utf-8'))
    assert saved_data['name'] == 'Saved Run'
    assert saved_data['cycle']['rate'] == 70.0
    assert saved_data['cycle']['duration'] == 10.0
    assert saved_data['cycle']['number'] == 3
    assert saved_data['performance_goals']['run_speed_target'] == 12.0
