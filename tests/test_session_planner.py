import pytest

from website.engine.session_planner import Session


def test_session_no_targets_leaves_calculated_fields_none():
    session = Session(cycle_rate=50, cycle_duration=30, number_of_cycles=4)

    assert session.performance_goals['run_speed_target'] is None
    assert session.performance_goals['walk_speed_target'] is None
    assert session.performance_goals['distance_target'] is None
    assert session.performance_goals['average_speed_target'] is None
    assert session.performance_goals['pace_target'] is None
    assert session.performance_goals['total_run_time'] == 60.0
    assert session.performance_goals['total_walk_time'] == 60.0
    assert session.performance_goals['total_session_time'] == 120.0


def test_session_only_run_speed_target_does_not_compute_average_or_distance():
    session = Session(cycle_rate=40, cycle_duration=20, number_of_cycles=3, run_speed_target=9.0)

    assert session.performance_goals['run_speed_target'] == 9.0
    assert session.performance_goals['walk_speed_target'] is None
    assert session.performance_goals['distance_target'] is None
    assert session.performance_goals['average_speed_target'] is None
    assert session.performance_goals['pace_target'] is None


def test_session_only_walk_speed_target_does_not_compute_average_or_distance():
    session = Session(cycle_rate=60, cycle_duration=15, number_of_cycles=2, walk_speed_target=6.0)

    assert session.performance_goals['run_speed_target'] is None
    assert session.performance_goals['walk_speed_target'] == 6.0
    assert session.performance_goals['distance_target'] is None
    assert session.performance_goals['average_speed_target'] is None
    assert session.performance_goals['pace_target'] is None


def test_session_with_run_and_walk_speed_targets_computes_average_and_distance():
    session = Session(cycle_rate=50, cycle_duration=30, number_of_cycles=4, run_speed_target=10.0, walk_speed_target=5.0)

    assert session.performance_goals['average_speed_target'] == pytest.approx(7.5)
    assert session.performance_goals['pace_target'] == pytest.approx(8.0)
    assert session.performance_goals['distance_target'] == pytest.approx(15.0)
    assert session.calculate_total_distance() == pytest.approx(15.0)
    assert session.calculate_total_time() == pytest.approx(120.0)
    assert session.calculate_run_walk_ratio() == pytest.approx(1.0)
    assert session.calculate_pace() == pytest.approx(8.0)


def test_session_with_distance_and_run_speed_target_computes_missing_walk_speed():
    session = Session(cycle_rate=50, cycle_duration=30, number_of_cycles=4, run_speed_target=10.0, distance_target=15.0)

    assert session.performance_goals['average_speed_target'] == pytest.approx(7.5)
    assert session.performance_goals['pace_target'] == pytest.approx(8.0)
    assert session.performance_goals['walk_speed_target'] == pytest.approx(5.0)
    assert session.performance_goals['distance_target'] == pytest.approx(15.0)


def test_session_with_distance_and_walk_speed_target_computes_missing_run_speed():
    session = Session(cycle_rate=50, cycle_duration=30, number_of_cycles=4, walk_speed_target=5.0, distance_target=15.0)

    assert session.performance_goals['average_speed_target'] == pytest.approx(7.5)
    assert session.performance_goals['pace_target'] == pytest.approx(8.0)
    assert session.performance_goals['run_speed_target'] == pytest.approx(10.0)
    assert session.performance_goals['distance_target'] == pytest.approx(15.0)


def test_session_with_only_distance_target_computes_average_and_pace():
    session = Session(cycle_rate=40, cycle_duration=20, number_of_cycles=3, distance_target=12.0)

    expected_average_speed = 12.0 / (session.performance_goals['total_session_time'] / 60)
    assert session.performance_goals['average_speed_target'] == pytest.approx(expected_average_speed)
    assert session.performance_goals['pace_target'] == pytest.approx(60.0 / expected_average_speed)
    assert session.performance_goals['run_speed_target'] is None
    assert session.performance_goals['walk_speed_target'] is None


def test_session_with_all_three_targets_warns_on_inconsistent_distance(capsys):
    session = Session(
        cycle_rate=50,
        cycle_duration=30,
        number_of_cycles=4,
        run_speed_target=10.0,
        walk_speed_target=5.0,
        distance_target=16.0,
    )

    assert session.performance_goals['average_speed_target'] == pytest.approx(7.5)
    assert session.performance_goals['pace_target'] == pytest.approx(8.0)
    captured = capsys.readouterr()
    assert 'Warning: The provided targets may be inconsistent.' in captured.out


def test_session_to_dict_and_from_dict_round_trip():
    original = Session(
        cycle_rate=60,
        cycle_duration=20,
        number_of_cycles=3,
        session_name='Benchmark',
        run_speed_target=9.0,
        walk_speed_target=6.0,
    )

    data = original.to_dict()
    round_trip = Session.from_dict(data)

    assert round_trip == original
    assert round_trip.name == 'Benchmark'
    assert round_trip.cycle == original.cycle


def test_session_from_dict_raises_when_cycle_missing():
    with pytest.raises(ValueError, match='Missing required field: cycle'):
        Session.from_dict({'name': 'Bad Session'})


def test_session_equality_with_non_session_returns_false():
    session = Session(cycle_rate=50, cycle_duration=10, number_of_cycles=2)
    assert not (session == object())
