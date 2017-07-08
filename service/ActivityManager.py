from stravalib.client import Client
import sqlite3
import arrow
import ConfigService

DBNAME = 'main.db'

# Create a strava Client
def getStravaClient():
    client = Client()
    client.access_token = ConfigService.getConfigVar('strava.access_token')
    print client.access_token

    return client

def getActvitesFromAPI(afterDate = '2016-01-1'):
    client = getStravaClient()
    a = []
    for activity in client.get_activities(after = afterDate,  limit=200):
        a.append(activity)
    return a

def fetchAllDb(sql, params=None):
    c, conn = getDbCCursor()

    if params:
        c.execute(sql, params)
    else :
        c.execute(sql)

    # Get column names
    names = [description[0] for description in c.description]
    
    # Get results from the db
    # Map each column in the row, to the associated column name
    results = []
    for row in c.fetchall():
        results.append(dict(zip(names, row)))
   
    closeConnection(conn)

    return results

def getDbCCursor():
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    return c, conn

def closeConnection(conn):
    conn.commit()
    conn.close()

def insertDb(sql, params):
    c, conn = getDbCCursor()

    if params:
        c.execute(sql, params)
    else :
        c.execute(sql)
   
    closeConnection(conn)
    return

def getAllStoredActivities(afterDate = '2016-0-01'):
    sql = """
    select * 
    from tb_activity;
    """

    return fetchAllDb(sql)

def getActivityType(activity):
    exerciseTypes = {
           'Run': 0,
           'Ride': 1,
           'Swim': 2,
           'EBikeRide' : 3,
           'Workout' : 4,
           'WeightTraining' : 5             
        }
    return exerciseTypes[activity.type]

def storeActivity(activity):  
    # Save startdate as iso format for consistancy
    startDate = arrow.get(activity.start_date)

    sql = """
        insert or ignore into tb_activity (
            fk_strava_activity_id,
            start_date,
            name,
            type
        ) values (
            ?,
            ?,
            ?,
            ?
        );
    """

    return insertDb(sql, (activity.id, startDate.format(), activity.name, getActivityType(activity)))

     