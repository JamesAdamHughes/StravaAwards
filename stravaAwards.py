from emailUtilities import sendEmail, getEmailServer
from stravalib.client import Client
from StravaConsistancyAward import StravaConsistancyAward
from pprint import pprint
import arrow
import ActivityManager
import AwardManager


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
    stravaActivites = ActivityManager.getActvitesFromAPI(ActivityManager.getStravaClient())
    for activity in stravaActivites:
        ActivityManager.storeActivity(activity)


print 'Starting Strava Awards'

# create clients
# smtpserver = getEmailServer()
stravaAwards = createAwards()

getAndStoreActivites()

# Go through awards and award them
for award in stravaAwards:
    occured = testAwardOccured(award)
    if occured:
        print award.getAwardText()    
        print 'Sending Email...'
        # sendEmail(smtpserver, award.name, award.getAwardText())
    print '\n'



