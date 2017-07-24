import arrow
from datetime import datetime, timedelta

class StravaAward:

    def __init__(self, name, eD, eW, eM, message, eT):
        self.epochDays          = eD
        self.epochWeeks         = eW
        self.epochMonths        = eM
        self.name               = name
        self.message            = message        
        self.exerciseType = eT
        
        # Setup datetime used as "now", using timezone aware date
        self.now = arrow.utcnow()


    def check_occured(self):
        """
        Defines the logic that controls if this award is run
        """
        pass

    
    def getStartDate(self):
        """
        Return the starting range of the award
        This should be the date of the start of the previous week or the previous month,
        The start of the week is monday
        """
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
        exercise_types = {
            0: 'Run',
            1: 'Ride'
        }
        return exercise_types[self.exerciseType]

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
        """
        Returns dict of object properties
        """
        return {
            "name" : self.name,
            "award_text" : self.getAwardText(),
            "start_date": self.getStartDate(),
            "end_date" : self.getEndDate(),
            "award_type" : self.getAwardType()
        }
    
    