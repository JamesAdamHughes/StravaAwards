from StravaAwards.service import DatabaseManager
from StravaAwards.model.User import User

import sys

def add_user(json_res):
    """
    Adds the strava user to the database
    """
    result = {'ok' : False}

    athlete = json_res["athlete"]

    # check if user already exists
    if len(get_user(athlete["id"])) > 0:
        result['ok'] = False
        result['message'] = "User already authed, can't add user again."
    else:
        user = User(athlete["id"], athlete["email"], athlete["firstname"], athlete["lastname"], athlete["profile"], athlete["sex"], json_res["access_token"])
        user.save()
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

    return result

