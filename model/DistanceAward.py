import arrow
from datetime import timedelta
from StravaAwards.model.StravaAward import StravaAward

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

    def awardLogic(self):
        """
        Defines the logic that controls if this award is run
        """

        sql = """
        select count(*) 
            from tb_activity             
        ;
        """

        return sql