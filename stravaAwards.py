from emailUtilities import sendEmail, getEmailServer
from stravalib.client import Client
from StravaConsistancyAward import StravaConsistancyAward, UTC
from pprint import pprint
import arrow
import ActivityManager


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
def testAwardOccured(award, activites):
    print "Checking " + award.name

    # Force set date for testing
    award.setNow(2017, 05, 30)

    print "Award time range: " + str(award.getStartDate()) + " to " + str(award.getEndDate());
    print arrow.get(award.getStartDate()).humanize()

    print "Valid Activites are..."
    validActivities = []
    for activity in activites:

        activityStartDate = arrow.get(activity.start_date)

        # Activity happened between now and now-eligiabletime
        if(activityStartDate > award.getStartDate() and activityStartDate < award.getEndDate()):
            if activity.type == award.getAwardType():
                print '\t' + activity.name
                validActivities.append(activity)

    print "valid activites : " + str(len(validActivities))

    if len(validActivities) == award.requiredActivites:
        print award.getAwardText()        
        return True
    else:
        return False


print 'Starting Strava Awards'

# create clients
smtpserver = getEmailServer()
stravaAwards = createAwards()

# Get and save activitys to database
stravaActivites = ActivityManager.getActvitesFromAPI(ActivityManager.getStravaClient())
for activity in stravaActivites:
    ActivityManager.storeActivity(activity)

# Go through awards and award them
for award in stravaAwards:
    occured = testAwardOccured(award, stravaActivites)
    if occured:
        print 'Sending Email...'
        sendEmail(smtpserver, award.name, award.getAwardText())
    print '\n'



