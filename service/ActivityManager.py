from stravalib.client import Client
import sqlite3
import arrow
from service import ConfigService
from service.Activity import Activity

DBNAME = 'main.db'

# Create a strava Client
def getStravaClient():
    client = Client()
    client.access_token = ConfigService.getConfigVar('strava.access_token')
    print client.access_token

    return client

def get_actvites_from_api(after_date='2016-01-1', limit=200):
    """
    Returns a list of user activites created after the after date
    """
    print after_date
    client = getStravaClient()
    activites = []
    for activity in client.get_activities(after=after_date, limit=limit):
        activites.append(Activity(activity.id, activity.name, activity.start_date, activity.type))

    return activites

def get_and_save_actvites_from_api(after_date='2016-01-1'):
    activites = get_actvites_from_api(after_date)
    result = [store_activity(a) for a in activites]
    return activites

def fetchAllDb(sql, params=None):
    c, conn = getDbCCursor()

    if params:
        c.execute(sql, params)
    else:
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
    return exerciseTypes[activity.type_id]

def store_activity(activity):  
    """
    Save startdate as iso format for consistancy
    """
    start_date = arrow.get(activity.start_date)
    print "[activityM] saving activity: " + str(activity.serialize())

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
  
    return insertDb(sql, (activity.fk_strava_activity_id, start_date.format(), activity.name, getActivityType(activity)))

     