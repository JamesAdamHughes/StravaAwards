from datetime import datetime, timedelta, tzinfo
import arrow

class StravaConsistancyAward:   

    def __init__ (self, name, eD, eW, eM, message, requiredActivites, requiredActivitesPerWeek, eT):
        self.epochDays          = eD
        self.epochWeeks         = eW
        self.epochMonths        = eM
        self.name               = name
        self.message            = message
        self.requiredActivites  = requiredActivites
        self.requiredActivitesPerWeek = requiredActivitesPerWeek
        self.exerciseType = eT
        
        # Setup datetime used as "now", using timezone aware date
        self.now = arrow.utcnow()

    # Defines the logic that controls if this award is run
    def awardLogic(self):

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
        """.format(self.getStartDate(), self.getEndDate(), self.exerciseType, self.requiredActivitesPerWeek)
        
        return sql

    # Return the starting range of the award
    # This should be the date of the start of the previous week or the previous month,
    # The start of the week is monday
    def getStartDate(self):
        date = None

        if (self.epochDays != 0):
            date = self.now - timedelta(days=self.epochDays)
        elif (self.epochWeeks != 0):
            date = self.now - timedelta(days=self.now.weekday(), weeks=(1 * (self.epochWeeks-1)))
        else:
            date = self.now - timedelta(days=self.now.weekday(), weeks=self.epochMonths*4)

        return date.format("YYYY-MM-DD 00:00:00")

    # Can't win awards for exercises done after "now"
    def getEndDate(self):
        # TODO make this work for weeks and month
        if (self.epochDays != 0):
            date = arrow.get(self.getStartDate()) + timedelta(days=self.epochDays)
        elif (self.epochWeeks != 0):
            date = arrow.get(self.getStartDate()) + timedelta(weeks=(1 * (self.epochWeeks))) - timedelta(days=1)
        else:
            # TODO make this work
            date = self.now - timedelta(days=self.now.weekday(), weeks=self.epochMonths*4)
        # date = arrow.get(self.getStartDate()) + timedelta(days=6)
        return date.format("YYYY-MM-DD 23:59:59")


    def getAwardType(self):
        exerciseTypes = {
            0: 'Run',
            1: 'Ride'
        }
        return exerciseTypes[self.exerciseType]

    def getAwardText(self):
        return 'You won a {0} Award! {1}'.format(self.name, self.message)


    def set_now(self, date):
        """
        Manually set the time of "now"
        Used for testing different dates. Default is UTC
        """     
        self.now = arrow.get(date, 'YYYY-M-D HH:mm:ss').replace(tzinfo='local')     
        return
    
    def serialize(self):
        return {
            "name" : self.name,
            "award_text" : self.getAwardText(),
            "start_date": self.getStartDate(),
            "end_date" : self.getEndDate(),
            "required_activites": self.requiredActivites
        }


