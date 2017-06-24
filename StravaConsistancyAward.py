from datetime import datetime, timedelta, tzinfo
import arrow

class StravaConsistancyAward:   

    def __init__ (self, name, eD, eW, eM, message, requiredActivites, eT):
        self.epochDays          = eD
        self.epochWeeks         = eW
        self.epochMonths        = eM
        self.name               = name
        self.message            = message
        self.requiredActivites  = requiredActivites
        self.exerciseType = eT
        
        # Setup datetime used as "now", using timezone aware date
        utc = UTC()
        self.now = datetime.now(utc)

    # Defines the logic that controls if this award is run
    def awardLogic(self):
        pass

    # Return the starting range of the award
    # This should be the date of the start of the previous week or the previous month, 
    # The start of the week is monday
    def getStartDate(self):
        if (self.epochDays != 0):
            return self.now - timedelta(days=self.epochDays)
        elif (self.epochWeeks != 0):
            return self.now - timedelta(days=self.now.weekday(), weeks=(1 * (self.epochWeeks-1)))
        else:
            return self.now - timedelta(days=self.now.weekday(), weeks=self.epochMonths*4)

    # Can't win awards for exercises done after "now"
    def getEndDate(self):
        return self.now

    def getAwardType(self):
        exerciseTypes = {
            0: 'Run',
            1: 'Ride'
        }
        return exerciseTypes[self.exerciseType]

    def getAwardText(self):
        return 'You won a {0} Award! {1}'.format(self.name, self.message)

    # Manually set the time of "now"
    # Used for testing different dates. Default is UTC
    def setNow(self, year, month, day):        
        string = datetime(year, month, day).isoformat(' ')
        self.now = arrow.get(string, 'YYYY-M-D HH:mm:ss').replace(tzinfo='local')     
        return   

# A UTC class.
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        ZERO = timedelta(0)
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        ZERO = timedelta(0)
        return ZERO



