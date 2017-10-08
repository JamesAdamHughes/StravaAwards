from datetime import datetime, timedelta, tzinfo
import arrow

class Activity:
    def __init__ (self, strava_id, name, user_id, start_date, type_id, distance, moving_time):
        self.fk_strava_activity_id = strava_id
        self.fk_strava_user_id = user_id
        self.name = name
        self.start_date = start_date
        self.type_id = type_id
        self.distance = distance
        self.moving_time = moving_time

    def serialize(self):
        """
        Returns a dict of an object
        """
        return {
            "fk_strava_activity_id": self.fk_strava_activity_id,
            "name": self.name,
            "strava_user_id" : self.fk_strava_user_id,
            "start_date": self.start_date,
            "distance" : self.distance,
            "moving_time": self.moving_time,
            "type_id": self.type_id
        }

    def get_activity_type(self):
        exercise_types = {
            'Run': 0,
            'Ride': 1,
            'Swim': 2,
            'EBikeRide' : 3,
            'Workout' : 4,
            'WeightTraining' : 5
            }
        return exercise_types[self.type_id]
        