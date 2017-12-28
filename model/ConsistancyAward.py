from StravaAwards.model.StravaAward import StravaAward
from StravaAwards.service import DatabaseManager

class ConsistancyAward(StravaAward):   

    def __init__ (self, name, eD, eW, eM, message, required_activites, required_activites_per_week, eT):
        self.required_activites = required_activites
        self.required_activites_per_week = required_activites_per_week
        self.award_class = 2
        StravaAward.__init__(self, name, eD, eW, eM, message, eT, award_class=self.award_class)


    def serialize(self):
        """
        Returns dict of object properties
        """
        obj = StravaAward.serialize(self)
        obj["required_activites"] = self.required_activites
        obj["required_activites_per_week"] = self.required_activites_per_week

        return obj


    def check_occured(self, strava_user_id):
        """
        Defines the logic that controls if this award is run
        """

        sql = """
        select count(*) as count, weekNo as weekNo from (
            select strftime('%W', start_date) weekNo, count(*)
            from tb_activity
                where 1=1
                    and start_date > ?
                    and start_date < ?
                    and type = ?
                    and fk_strava_user_id = ?
            group by weekNo
            having count(*) >= ?
        );
        """
        params = [self.getStartDate(), self.getEndDate(), self.exerciseType, strava_user_id, self.required_activites_per_week]

        activites = DatabaseManager.fetch_one(sql, params)

        # check if the required no of acvities exist,
        # Also check if the same award has already been given
        if activites[0]['count'] == self.required_activites:
            print "[award] AWARD REQUIREMENTS MET"
            return True

        print "[award] not enough new activities" + str(activites)
        return False

