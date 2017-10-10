import arrow
from StravaAwards.service import DatabaseManager

class User(object):

    def __init__(self, strava_id, email, fname, lname, profile, gender, token):
        self.strava_id = strava_id
        self.email_address = email
        self.f_name = fname
        self.l_name = lname
        self.profile_image_url = profile        
        self.gender = gender
        self.access_token = token        

    
