from StravaAwards.service import DatabaseManager, SubscriptionManager
from StravaAwards.model.User import User

import sys

def add_user(json_res):
    """
    Adds the strava user to the database. Adds subscription to user events
    """
    
    result = {'ok' : False}
    athlete = json_res["athlete"]

    # check if user already exists
    user = get_user(athlete["id"])
    if user:
        result['ok'] = False
        result['message'] = "User already authed, can't add user again."
        result['user'] = user
    else:
        # create user object and save
        user = User(athlete["id"], athlete["email"], athlete["firstname"], athlete["lastname"], athlete["profile"], athlete["sex"], json_res["access_token"])
        user.save()

        #subscribe user to events
        SubscriptionManager.subscribe
        
        result['ok'] = True
        result['message'] = 'User added successfully'
        result['user'] = user
    
    return result

def get_user(strava_user_id):
    sql = """
    select * 
    from tb_user 
    where 1=1
        and fk_strava_user_id=?
    """

    params = [strava_user_id]
    
    result = DatabaseManager.fetch_one(sql, params)
    print result

    if len(result) == 0:
        return False

    fields = result[0]
    return User(
        fields['fk_strava_user_id'], 
        fields['email_address'],
        fields['first_name'],
        fields['last_name'],
        fields['profile_image_url'],
        fields['gender'],
        fields['access_token']        
    )

