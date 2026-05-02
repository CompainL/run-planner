class Session:
    def __init__(self, cycle_rate, cycle_duration, number_of_cycles, session_name=None, run_speed_target=None, walk_speed_target=None, distance_target=None):
        self.name = session_name
        self.cycle = {
            'rate': cycle_rate,
            'duration': cycle_duration,
            'number': number_of_cycles
        }
        self.performance_goals = {
            'run_speed_target': run_speed_target if run_speed_target is not None else None, # in km/h, check if provided, if not set to None
            'walk_speed_target': walk_speed_target if walk_speed_target is not None else None, # in km/h, check if provided, if not set to None
            'distance_target': distance_target if distance_target is not None else None, # in km, check if provided, if not set to None
            'total_run_time': (cycle_duration * number_of_cycles * cycle_rate) /100 if cycle_rate > 0 else None, # in minutes, calculated based on cycle rate and total session time, if cycle rate is 0, set to None
            'total_walk_time': (cycle_duration * number_of_cycles * (100 - cycle_rate)) /100 if cycle_rate < 100 else None, # in minutes, calculated based on cycle rate and total session time, if cycle rate is 100, set to None
            'total_session_time': cycle_duration * number_of_cycles, # in minutes, calculated based on cycle duration and number of cycles
            'average_speed_target': None, # in km/h, calculated based on run and walk speed targets and cycle rate, or based on distance target and total session time, if neither are provided, set to None
            'pace_target': None # in min/km, calculated based on average speed target, if average speed target is not provided, set to None
        }
        self.calculate_missing_parameters() # calculate any missing parameters based on the provided data

    def to_dict(self):
        # This method converts the Session object to a dictionary format. It includes all the attributes of the session, including the name, cycle details, and performance goals. This is useful for serialization and for passing the session data to templates or APIs.
        return {
            'name': self.name,
            'cycle': self.cycle,
            'performance_goals': self.performance_goals
        }
    
    def from_dict(data):
        # This method creates a Session object from a dictionary. It checks for the presence of all required fields and raises an error if any are missing. It also handles optional fields and sets them to None if they are not provided.
        required_fields = ['cycle']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        return Session(
            cycle_rate=data['cycle']['rate'],
            cycle_duration=data['cycle']['duration'],
            number_of_cycles=data['cycle']['number'],
            session_name=data.get('name'),
            run_speed_target=data['performance_goals'].get('run_speed_target'),
            walk_speed_target=data['performance_goals'].get('walk_speed_target'),
            distance_target=data['performance_goals'].get('distance_target')
        )   
    
    def __str__(self):
        return f"Session(name={self.name}, cycle_rate={self.cycle['rate']}%, cycle_duration={self.cycle['duration']} min, number_of_cycles={self.cycle['number']}, total_run_time={self.performance_goals['total_run_time']} min, total_walk_time={self.performance_goals['total_walk_time']} min, total_session_time={self.performance_goals['total_session_time']} min, average_speed_target={self.performance_goals['average_speed_target']} km/h, pace_target={self.performance_goals['pace_target']} min/km, distance_target={self.performance_goals['distance_target']} km), run_speed_target={self.performance_goals['run_speed_target']} km/h, walk_speed_target={self.performance_goals['walk_speed_target']} km/h)"

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Session):
            return False
        return self.to_dict() == other.to_dict()
    
    def calculate_total_distance(self):
        # This method calculates the total distance of the session based on the average speed target and total session time
        if self.performance_goals['average_speed_target'] and self.performance_goals['total_session_time']:
            return (self.performance_goals['average_speed_target'] * (self.performance_goals['total_session_time'] / 60)) # in km, calculated based on average speed target and total session time
        return None
    
    def calculate_total_time(self):
        # This method calculates the total time of the session based on the distance target and average speed target
        if self.performance_goals['distance_target'] and self.performance_goals['average_speed_target']:
            return (self.performance_goals['distance_target'] / self.performance_goals['average_speed_target']) * 60 # in minutes, calculated based on distance target and average speed target
        return None
    
    def calculate_pace(self):
        # This method calculates the pace of the session based on the average speed target
        if self.performance_goals['average_speed_target']:
            return 60 / self.performance_goals['average_speed_target'] # in min/km, calculated based on average speed target
        return None
    
    def calculate_run_walk_ratio(self):
        # This method calculates the run/walk ratio of the session based on the cycle rate
        if self.cycle['rate'] > 0 and self.cycle['rate'] < 100:
            return self.cycle['rate'] / (100 - self.cycle['rate'])
        return None
    
    def calculate_average_speed(self):
        # This method calculates the average speed of the session based on the run and walk speed targets and the cycle rate
        if self.performance_goals['run_speed_target'] and self.performance_goals['walk_speed_target']: 
            # If both run and walk speed targets are provided, calculate average speed as a weighted average based on the cycle rate
            return (self.performance_goals['run_speed_target'] * (self.cycle['rate'] / 100)) + (self.performance_goals['walk_speed_target'] * ((100 - self.cycle['rate']) / 100))
        elif self.performance_goals['distance_target'] and self.performance_goals['total_session_time']:
            # If distance target and total session time are provided, calculate average speed based on distance and time
            return (self.performance_goals['distance_target'] / (self.performance_goals['total_session_time'] / 60)) # in km/h, calculated based on distance target and total session time
        return None


    def calculate_missing_parameters(self):
        # This method calculates any missing parameters based on the available data
        # The following values are always none when the session is created: average_speed_target, pace_target. They cannot be provided by the user and are always calculated based on the following logic:
        # The following values may be none when the session is created: run_speed_target, walk_speed_target, distance_target. They can be provided by the user but are not required. 

        # They are calculated based on the following logic:
        # If none of the above are provided, average_speed_target and pace_target cannot be calculated and remain None
        # If only run_speed_target is provided, the others will not be calculated as we cannot determine the walk speed target or the average speed target without more information
        # If only walk_speed_target is provided, the others will not be calculated as we cannot determine the run speed target or the average speed target without more information
        # If both run_speed_target and walk_speed_target are provided, average_speed_target is calculated as a weighted average based on the cycle rate and pace target is calculated based on the average speed target. distance_target is calculated based on the average speed target and total session time
        # If distance target and only one of the speed targets are provided, the missing speed target is calculated based on the average speed target and cycle rate, and pace target is calculated based on the average speed target. If distance target is provided but neither speed target is provided, both speed targets are calculated based on the average speed target and cycle rate, and pace target is calculated based on the average speed target.
        # If only distance_target is provided, average_speed_target is calculated based on the distance target and total session time, and pace target is calculated based on the average speed target. Run and walk speed targets are noy calculated as we cannot determine the split between run and walk without more information.
        # If all three are provided, there may be inconsistencies in the data. 

        # case 1: no targets provided
        if not self.performance_goals['run_speed_target'] and not self.performance_goals['walk_speed_target'] and not self.performance_goals['distance_target']:
            self.performance_goals['average_speed_target'] = None # in km/h, cannot be calculated without any targets
            self.performance_goals['pace_target'] = None # in min/km, cannot be calculated without any targets
        # case 2: only run speed target provided
        elif self.performance_goals['run_speed_target'] and not self.performance_goals['walk_speed_target'] and not self.performance_goals['distance_target']:
            self.performance_goals['average_speed_target'] = None # in km/h, cannot be calculated without walk speed target or distance target
            self.performance_goals['pace_target'] = None # in min/km, cannot be calculated without average speed target
        # case 3: only walk speed target provided   
        elif not self.performance_goals['run_speed_target'] and self.performance_goals['walk_speed_target'] and not self.performance_goals['distance_target']:
            self.performance_goals['average_speed_target'] = None # in km/h, cannot be calculated without run speed target or distance target
            self.performance_goals['pace_target'] = None # in min/km, cannot be calculated without average speed target
        # case 4: both run and walk speed targets provided
        elif self.performance_goals['run_speed_target'] and self.performance_goals['walk_speed_target'] and not self.performance_goals['distance_target']:
            self.performance_goals['average_speed_target'] = self.calculate_average_speed() # in km/h, calculated based on run and walk speed targets and cycle rate
            self.performance_goals['pace_target'] = self.calculate_pace() # in min/km, calculated based on average speed target
            self.performance_goals['distance_target'] = self.calculate_total_distance() # in km, calculated based on average speed target and total session time
        # case 5: distance target provided with one of the speed targets
        elif self.performance_goals['distance_target'] and (self.performance_goals['run_speed_target'] or self.performance_goals['walk_speed_target']) and not (self.performance_goals['run_speed_target'] and self.performance_goals['walk_speed_target']):
            self.performance_goals['average_speed_target'] = self.calculate_average_speed() # in km/h, calculated based on distance target and total session time
            self.performance_goals['pace_target'] = self.calculate_pace() # in min/km, calculated based on average speed target
            if self.performance_goals['run_speed_target'] and not self.performance_goals['walk_speed_target']:
                # If only run speed target is provided, calculate walk speed target based on average speed target and cycle rate
                run_distance = (self.performance_goals['run_speed_target'] * (self.performance_goals['total_run_time'] / 60)) if self.performance_goals['run_speed_target'] and self.performance_goals['total_run_time'] else None # in km, calculated based on run speed target and total run time
                walk_distance = self.performance_goals['distance_target'] - run_distance if self.performance_goals['distance_target'] and run_distance is not None else None # in km, calculated based on distance target and run distance
                walk_time = self.performance_goals['total_walk_time'] / 60 if self.performance_goals['total_walk_time'] else None # in hours, calculated based on total walk time
                self.performance_goals['walk_speed_target'] = (walk_distance / walk_time) if walk_distance is not None and walk_time is not None else None
            elif self.performance_goals['walk_speed_target'] and not self.performance_goals['run_speed_target']:
                # If only walk speed target is provided, calculate run speed target based on average speed target and cycle rate
                walk_distance = (self.performance_goals['walk_speed_target'] * (self.performance_goals['total_walk_time'] / 60)) if self.performance_goals['walk_speed_target'] and self.performance_goals['total_walk_time'] else None # in km, calculated based on walk speed target and total walk time
                run_distance = self.performance_goals['distance_target'] - walk_distance if self.performance_goals['distance_target'] and walk_distance is not None else None # in km, calculated based on distance target and walk distance
                run_time = self.performance_goals['total_run_time'] / 60 if self.performance_goals['total_run_time'] else None # in hours, calculated based on total run time
                self.performance_goals['run_speed_target'] = (run_distance / run_time) if run_distance is not None and run_time is not None else None # in km/h, calculated based on run distance and run time
            self.performance_goals['pace_target'] = self.calculate_pace() # in min/km, calculated based on average speed target
        # case 6: only distance target provided
        elif self.performance_goals['distance_target'] and not self.performance_goals['run_speed_target'] and not self.performance_goals['walk_speed_target']:
            self.performance_goals['average_speed_target'] = self.calculate_average_speed() # in km/h, calculated based on distance target and total session time
            self.performance_goals['pace_target'] = self.calculate_pace() # in min/km, calculated based on average speed target
            # run and walk speed targets cannot be calculated without more information about the split between run and walk, so they remain None
        # case 7: all three targets provided
        elif self.performance_goals['run_speed_target'] and self.performance_goals['walk_speed_target'] and self.performance_goals['distance_target']: 
            # If all three targets are provided, calculate average speed target based on run and walk speed targets and cycle rate, and pace target based on average speed target. Check for inconsistencies in the data by calculating the distance based on the average speed target and total session time and comparing it to the provided distance target. If there is a significant discrepancy, print a warning message.
            self.performance_goals['average_speed_target'] = self.calculate_average_speed() # in km/h, calculated based on run and walk speed targets and cycle rate
            self.performance_goals['pace_target'] = self.calculate_pace() # in min/km, calculated based on average speed target
            # check for inconsistencies
            calculated_distance = self.calculate_total_distance() # in km, calculated based on average speed target and total session time
            if abs(calculated_distance - self.performance_goals['distance_target']) > 0.1:  # allow for small margin of error
                print("Warning: The provided targets may be inconsistent. The calculated distance based on the run and walk speed targets does not match the provided distance target.")