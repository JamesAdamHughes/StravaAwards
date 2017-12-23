import arrow
from datetime import timedelta
from StravaAwards.model.StravaAward import StravaAward
from StravaAwards.service import DatabaseManager

class DistanceAward(StravaAward):

    def __init__ (self, name, eD, eW, eM, message, required_distance, eT):
        self.required_distance = required_distance
        StravaAward.__init__(self, name, eD, eW, eM, message, eT)

    def serialize(self):
        """
        Returns dict of object properties
        """
        obj = StravaAward.serialize(self)
        obj["required_distance"] = self.required_distance

        return obj

    def check_occured(self, strava_user_id):
        """
        Defines the logic that controls if this award is run
        """

        sql = """
        select sum(distance) as total_distance
        from tb_activity
        where 1=1
            and start_date > ?
            and start_date < ?
            and type = ?
            and fk_strava_user_id = ?
        """

        params = [self.getStartDate(), self.getEndDate(), self.exerciseType, strava_user_id]
        result = DatabaseManager.fetch_one(sql, params)

        if result[0]['total_distance'] >= self.required_distance:
            print result
            print "[award] AWARD REQUIREMENTS MET"
            return True

        return False