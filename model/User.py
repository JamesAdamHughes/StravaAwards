import arrow
from StravaAwards.service import DatabaseManager

class User(object):

    def __init__(self, id, email, fname, lname, profile, gender, token):
        self.user_id = id
        self.email_address = email
        self.f_name = fname
        self.l_name = lname
        self.profile_image_url = profile        
        self.gender = gender
        self.access_token = token        

    def save(self):
        '''
        Save user to database
        ''' 

        sql = """
        insert into tb_user (
        	fk_strava_user_id,
	        email_address,
	        first_name,
            last_name,
            gender,
            access_token,
            profile_image_url,
            datetime_created
            ) values (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            );
        """

        params = [self.user_id, self.email_address, self.f_name, self.l_name, self.gender, self.access_token, self.profile_image_url, arrow.now().format()]
        DatabaseManager.insert_db(sql, params)
            
        return
