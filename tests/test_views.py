from website import create_app


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

def test_make_plan_post_valid_input_shows_results():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/make_plan',
            data={
                'session_name': 'Test Session',
                'cycle_rate': '50',
                'cycle_duration': '30',
                'number_of_cycles': '4',
                'run_speed_target': '10',
                'walk_speed_target': '5',
                'distance_target': '5'
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Run Plan: Test Session' in response.data
    assert b'Cycle Rate: 50.0%' in response.data
    assert b'Cycle Duration: 30.0 minutes' in response.data
    assert b'Number of Cycles: 4' in response.data
    assert b'Run Speed Target: 10.0 km/h' in response.data
    assert b'Walk Speed Target: 5.0 km/h' in response.data
    assert b'Distance Target: 5.0 km' in response.data

def test_make_plan_post_invalid_input_shows_error():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/make_plan',
            data={
                'session_name': 'Test Session',
                'cycle_rate': '-50',
                'cycle_duration': '0',
                'number_of_cycles': '-1',
                'run_speed_target': '10',
                'walk_speed_target': '5',
                'distance_target': '5'
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Please enter valid positive numbers for all fields.' in response.data

def test_make_plan_post_blank_optional_fields_uses_none():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/make_plan',
            data={
                'session_name': 'Test Session',
                'cycle_rate': '50',
                'cycle_duration': '30',
                'number_of_cycles': '4',
                'run_speed_target': '',
                'walk_speed_target': '',
                'distance_target': ''
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Run Plan: Test Session' in response.data
    assert b'Cycle Rate: 50.0%' in response.data
    assert b'Cycle Duration: 30.0 minutes' in response.data
    assert b'Number of Cycles: 4' in response.data
    assert b'Run Speed Target: None' in response.data
    assert b'Walk Speed Target: None' in response.data
    assert b'Distance Target: None' in response.data

def test_make_plan_post_blank_optional_fields_with_valid_required_fields():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        response = client.post(
            '/make_plan',
            data={
                'session_name': 'Test Session',
                'cycle_rate': '50',
                'cycle_duration': '30',
                'number_of_cycles': '4',
                'run_speed_target': '',
                'walk_speed_target': '',
                'distance_target': ''
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b'Run Plan: Test Session' in response.data
    assert b'Cycle Rate: 50.0%' in response.data
    assert b'Cycle Duration: 30.0 minutes' in response.data
    assert b'Number of Cycles: 4' in response.data