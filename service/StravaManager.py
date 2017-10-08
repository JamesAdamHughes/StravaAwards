from stravalib.client import Client
from StravaAwards.service import ConfigService

# Create a strava Client
def get_strava_client():
    client = Client()
    client.access_token = ConfigService.getConfigVar('strava.access_token')
    print client.access_token

    return client