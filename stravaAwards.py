from stravalib.client import Client
from pprint import pprint
import arrow
from service import AwardManager, ActivityManager, emailUtilities, ConfigService, SubscriptionManager
from service.StravaConsistancyAward import StravaConsistancyAward
import subprocess

def createAwards():
    awards = []
    # todo write this up in json and read from file
    awards.append(StravaConsistancyAward('TwiceThisWeekAward', 0, 1, 0, 'You ran twice this week!', 2, 0))
    awards.append(StravaConsistancyAward('Once This Week', 0, 1, 0, 'You ran once this week!', 1, 0))
    awards.append(StravaConsistancyAward('TwoWeeksInARow', 0, 2, 0, 'You ran two weeks in a row!', 2, 0))
    awards.append(StravaConsistancyAward('Four times a Month', 0, 0, 1, 'You ran four times this month!', 4, 0))

    return awards


# Function takes an award type, applies it to the activites data
# returns true if the award occured
def testAwardOccured(award):
    print "Checking " + award.name

    # Force set date for testing
    award.setNow(2017, 06, 30)

    print "Award time range: " + str(award.getStartDate()) + " to " + str(award.getEndDate());
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

    # Create the list of valid awards that can be given out
    awards = createAwards()

    # Get list of all activites for a user and store them in a database
    # This is done on startup to ensure all activites are up to date
    # getAndStoreActivites()
    SubscriptionManager.subscribe()




    # Check if any awards need to be given out for recent activites


if __name__ == '__main__':
    # Run additional server
    # subprocess.call("./server/flask_setup", shell=True)

    # run main logic thread
    main()
