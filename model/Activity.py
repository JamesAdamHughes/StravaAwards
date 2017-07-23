from datetime import datetime, timedelta, tzinfo
import arrow

class Activity:
    def __init__ (self, strava_id, name, start_date, type_id):
        self.fk_strava_activity_id = strava_id
        self.name = name
        self.start_date = start_date
        self.type_id = type_id

    def serialize(self):
        """
        Returns a dict of an object
        """
        return {
            "fk_strava_activity_id": self.fk_strava_activity_id,
            "name": self.name,
            "start_date": self.start_date,
            "type_id": self.type_id
        }
        