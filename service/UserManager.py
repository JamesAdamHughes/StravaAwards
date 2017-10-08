from StravaAwards.service import ConfigService, DatabaseManager, StravaManager
import sys

def add_user(strava_user_id):
    """
    Adds the strava user to the database
    """
    client = StravaManager.get_strava_client()
    try:
        user = client.get_athlete(strava_user_id)
        print user
    except :
        the_type, the_value, the_traceback = sys.exc_info()
        print the_value

    return 'user'
