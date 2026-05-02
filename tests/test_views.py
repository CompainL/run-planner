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
