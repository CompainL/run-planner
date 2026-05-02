def Riegel_prediction(distance, time, target_distance):
    """
    Predicts the time for a target distance based on a known distance and time using Riegel's formula.

    Parameters:
    distance (float): The known distance (in meters).
    time (float): The time taken to cover the known distance (in seconds).
    target_distance (float): The target distance for which to predict the time (in meters).

    Returns:
    float: The predicted time for the target distance (in seconds).
    """
    exponent = 1.06  # Riegel's exponent
    predicted_time = time * (target_distance / distance) ** exponent
    return predicted_time

def Cameron_prediction(distance, time, target_distance):
    """
    Predicts the time for a target distance based on a known distance and time using Cameron's formula.

    Parameters:
    distance (float): The known distance (in meters).
    time (float): The time taken to cover the known distance (in seconds).
    target_distance (float): The target distance for which to predict the time (in meters).

    Returns:
    float: The predicted time for the target distance (in seconds).
    """
    exponent = 1.07  # Cameron's exponent
    predicted_time = time * (target_distance / distance) ** exponent
    return predicted_time

def both_predictions(distance, time, target_distance):
    """
    Predicts the time for a target distance using both Riegel's and Cameron's formulas.

    Parameters:
    distance (float): The known distance (in meters).
    time (float): The time taken to cover the known distance (in seconds).
    target_distance (float): The target distance for which to predict the time (in meters).

    Returns:
    dict: A dictionary containing the predicted times from both Riegel's and Cameron's formulas.
    """
    riegel_time = Riegel_prediction(distance, time, target_distance)
    cameron_time = Cameron_prediction(distance, time, target_distance)
    
    return {
        'Riegel': riegel_time,
        'Cameron': cameron_time
    }