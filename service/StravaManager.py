from stravalib.client import Client
from StravaAwards.service import ConfigService, UserManager

# Create a strava Client
def get_strava_client(user_id=None):

    client = Client()
    if user_id == None:
        client.access_token = ConfigService.getConfigVar('strava.access_token')
    else:
        user = UserManager.get_user(user_id)
        if user:
            client.access_token = user.access_token
    
    print client.access_token

    return client