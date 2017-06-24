from stravalib.client import Client
import sqlite3
import arrow

DBNAME = 'main.db'


# Create a strava Client
def getStravaClient():
    client = Client()
    client.access_token = 'eb7344dda517a55ca287f41e498005e13159cdc0'
    return client

def getActvitesFromAPI(client, afterDate = '2017-05-1'):
    a = []
    for activity in client.get_activities(after = afterDate,  limit=200):
        a.append(activity)
    return a

def getActivityType(activity):
    exerciseTypes = {
           'Run': 0,
           'Ride': 1             
        }
    return exerciseTypes[activity.type]

def storeActivity(activity):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    
    # Save startdate as iso format for consistancy
    startDate = arrow.get(activity.start_date)

    sql = """
        insert into tb_activity (
            fk_strava_activity_id,
            start_date,
            name,
            type
        ) values (
            {0},
            '{1}',
            '{2}',
            {3}
        );
    """.format(activity.id, startDate, activity.name, getActivityType(activity))

    c.execute(sql)
    
    conn.commit()
    conn.close()

    return 