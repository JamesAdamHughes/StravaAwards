from stravalib.client import Client
from StravaAwards.service import ConfigService, UserManager

# Create a strava Client
def get_strava_client(user_id=None):

    client = Client()
    if user_id is None:
        client.access_token = ConfigService.getConfigVar('strava.access_token')
    else:
        user = UserManager.get_user(user_id)
        if user:
            client.access_token = user.access_token
        else:
            print "[stravaM]: User {0} not found".format(user_id)
            return False

    return client