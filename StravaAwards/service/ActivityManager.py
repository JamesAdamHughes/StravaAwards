import arrow
from StravaAwards.service import DatabaseManager, StravaManager
from StravaAwards.model.Activity import Activity
def get_actvites_from_api(user_id, after_date, limit=200):
    """
    Returns a list of user activites created after the after date
    """

    activites = []
    client = StravaManager.get_strava_client(user_id=user_id)

    if not client:
        return []

    for activity in client.get_activities(after=after_date, limit=limit):
        activites.append(Activity(activity.id, activity.name, activity.athlete.id, activity.start_date, activity.type, activity.distance.get_num(), activity.moving_time.total_seconds()))

    return activites

def get_and_save_actvites_from_api(user_id, after_date=None):
    if after_date is None:
        after_date = arrow.now().replace(years=-1).format("YYYY-MM-DD")
    
    print "[activityM] after_date: " + after_date

    activites = get_actvites_from_api(user_id, str(after_date))
    print "[activityM] got this many activites: " + str(len(activites))
    [store_activity(a) for a in activites]
    return activites

def get_all_stored_activities(after_date='2016-0-01'):
    sql = """
    select * 
    from tb_activity;
    """

    return DatabaseManager.fetch_all(sql)

def store_activity(activity):
    """
    Save startdate as iso format for consistancy
    """
    start_date = arrow.get(activity.start_date)
    print "[activityM] saving activity: " + str(activity.serialize()["fk_strava_activity_id"])

    sql = """
        insert or ignore into tb_activity (
            fk_strava_activity_id,
            fk_strava_user_id,
            start_date,
            name,
            type,
            distance,
            moving_time
        ) values (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        );
    """
    params = [
        activity.fk_strava_activity_id,
        activity.fk_strava_user_id,
        start_date.format(),
        activity.name,
        activity.get_activity_type(),
        activity.distance,
        activity.moving_time
    ]
    return DatabaseManager.insert_db(sql, params)

