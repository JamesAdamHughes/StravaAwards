from StravaAwards.model.StravaAward import StravaAward
import arrow

class ConsistancyAward(StravaAward):   

    def __init__ (self, name, eD, eW, eM, message, required_activites, required_activites_per_week, eT):
        self.required_activites = required_activites
        self.required_activites_per_week = required_activites_per_week
        StravaAward.__init__(self, name, eD, eW, eM, message, eT)


    def serialize(self):
        """
        Returns dict of object properties
        """
        obj = StravaAward.serialize(self)
        obj["required_activites"] = self.required_activites
        obj["required_activites_per_week"] = self.required_activites_per_week

        return obj


    def awardLogic(self):
        """
        Defines the logic that controls if this award is run
        """

        sql = """
        select count(*) from (
            select strftime('%W', start_date) weekNo, count(*)
            from tb_activity
                where 1=1
                    and start_date > '{0}'
                    and start_date < '{1}'
                    and type = {2}
            group by weekNo
            having count(*) = {3}
        );
        """.format(self.getStartDate(), self.getEndDate(), self.exerciseType, self.required_activites_per_week)

        return sql


