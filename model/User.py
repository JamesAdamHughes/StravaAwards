import arrow
from datetime import datetime, timedelta

class User:

    def __init__(self, name, eD, eW, eM, message, eT):
        self.epochDays          = eD
        self.epochWeeks         = eW
        self.epochMonths        = eM
        self.name               = name
        self.message            = message        
        self.exerciseType = eT
        
        # Setup datetime used as "now", using timezone aware date
        self.now = arrow.utcnow()


    