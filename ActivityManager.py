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

def fetchAllDb(sql, params=None):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

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
   
    conn.commit()
    conn.close()

    return results

def insertDb(sql, params):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    if params:
        c.execute(sql, params)
    else :
        c.execute(sql)
   
    conn.commit()
    conn.close()

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
           'Ride': 1             
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

     