import pytest

from website.engine.utils.predictions import (
    Riegel_prediction,
    Cameron_prediction,
    both_predictions,
)


def test_riegel_prediction_known_values():
    distance = 5000.0  # meters
    time = 1500.0  # seconds (25 minutes)
    target_distance = 10000.0  # meters

    expected = time * (target_distance / distance) ** 1.06
    result = Riegel_prediction(distance, time, target_distance)

    assert pytest.approx(result, rel=1e-9) == expected


def test_cameron_prediction_known_values():
    distance = 5000.0
    time = 1500.0
    target_distance = 10000.0

    expected = time * (target_distance / distance) ** 1.07
    result = Cameron_prediction(distance, time, target_distance)

    assert pytest.approx(result, rel=1e-9) == expected


def test_both_predictions_matches_individual_functions():
    distance = 10000.0
    time = 3600.0
    target_distance = 21097.5

    result = both_predictions(distance, time, target_distance)

    assert set(result.keys()) == {'Riegel', 'Cameron'}
    assert result['Riegel'] == pytest.approx(Riegel_prediction(distance, time, target_distance), rel=1e-9)
    assert result['Cameron'] == pytest.approx(Cameron_prediction(distance, time, target_distance), rel=1e-9)


def test_prediction_returns_same_time_for_same_distance():
    distance = 10000.0
    time = 2500.0
    target_distance = distance

    riegel = Riegel_prediction(distance, time, target_distance)
    cameron = Cameron_prediction(distance, time, target_distance)

    assert pytest.approx(riegel, rel=1e-9) == time
    assert pytest.approx(cameron, rel=1e-9) == time
