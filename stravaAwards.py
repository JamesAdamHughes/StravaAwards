from stravalib.client import Client
from pprint import pprint
import arrow
from service import AwardManager, ActivityManager, emailUtilities, ConfigService, SubscriptionManager
from service.StravaConsistancyAward import StravaConsistancyAward
import subprocess
from flask import Flask, request
from server.routes import stravaRoute
from server.CustomJSONEncoder import CustomJSONEncoder

app = Flask('server')
app.json_encoder = CustomJSONEncoder
app.register_blueprint(stravaRoute)
print '[server] server running at :5000'

# Function takes an award type, applies it to the activites data
# returns true if the award occured
def testAwardOccured(award):
    print "Checking " + award.name

    # Force set date for testing
    award.setNow(2017, 06, 30)

    print "Award time range: " + str(award.getStartDate()) + " to " + str(award.getEndDate())
    print arrow.get(award.getStartDate()).humanize()

    return AwardManager.checkAwardOccured(award)

# Get and save activitys to database
def getAndStoreActivites():
    print '[main] getting activites'
    stravaActivites = ActivityManager.getActvitesFromAPI()
    print '[main] got ' + str(len(stravaActivites)) + ' activities, storing...'
    for activity in stravaActivites:
        ActivityManager.storeActivity(activity)



# create clients
# smtpserver = getEmailServer()
# stravaAwards = createAwards()


# # Go through awards and award them
# for award in stravaAwards:
#     occured = testAwardOccured(award)
#     if occured:
#         print award.getAwardText()    
#         print 'Sending Email...'
#         # sendEmail(smtpserver, award.name, award.getAwardText())
#     print '\n'


########
# Start of main program
# Check if any old awards to be given
# Subscribe to webhook events
########
def main():
    print '[main] Starting Strava Awards'
    # server.run()
    # Create the list of valid awards that can be given out
    awards = AwardManager.createAwards()

    # Get list of all activites for a user and store them in a database
    # This is done on startup to ensure all activites are up to date
    # getAndStoreActivites()
    SubscriptionManager.subscribe()




    # Check if any awards need to be given out for recent activites

# if __name__ == '__main__':
    # Run additional server
    # subprocess.call("./server/flask_setup", shell=True)

    # run main logic thread
    # main()

# app.run(host='0.0.0.0', port=5000, debug=False)
# 

