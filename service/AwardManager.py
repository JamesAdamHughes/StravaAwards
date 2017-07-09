import sqlite3
from StravaConsistancyAward import StravaConsistancyAward
import arrow

DBNAME = 'main.db'

def check_award_occured(award):
    """
    Runs the award logic for an award, to test if it has occured
    Currently only works with SQL statements and consistancy awards
    """
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    # select from the database as needed
    award_sql = award.awardLogic()

    c.execute(award_sql)

    # Probably should put this in the award object itself
    result = c.fetchone()

    conn.commit()
    conn.close()

    # check if the required no of acvities exist, 
    # Also check if the same award has already been given
    if result[0] == award.requiredActivites:
        return True
    else:
        return False


def get_award_from_db(start_date, end_date, type):
    """
    Returns an award from the database, using the start end and type as a unique identifier
    """
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    sql = """
    select top 1 * from tb_award where
    """


def save_award(award, user_id):
    """
    Takes an award and saves ti to the db
    """
    print "[awardM] saving award: " + str(award.name)
    return add_award_to_db(user_id, award)


def add_award_to_db(user_id, award):
    """
    Inserts an award into tb_award
    """
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    sql = """
        insert into tb_award (
            fk_user_id,
            name,
            datetime_start,
            datetime_end,
            type_id,
            datetime_created
        ) values (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        );
    """

    result = c.execute(sql, [user_id, award.name, award.getStartDate(), award.getEndDate(), award.getAwardType(), arrow.now().format()])  

    conn.commit()
    conn.close() 
    return


def createAwards():
    """
    Return a list of strava award types
    """
    awards = []
    # todo write this up in json and read from file
    awards.append(StravaConsistancyAward('TwiceThisWeekAward', 0, 1, 0, 'You ran twice this week!', 2, 0))
    awards.append(StravaConsistancyAward('Once This Week', 0, 1, 0, 'You ran once this week!', 1, 0))
    awards.append(StravaConsistancyAward('TwoWeeksInARow', 0, 2, 0, 'You ran two weeks in a row!', 2, 0))
    awards.append(StravaConsistancyAward('Four times a Month', 0, 0, 1, 'You ran four times this month!', 4, 0))

    return awards


def test_award_occured(award, now_date="2017-07-09"):
    """
    Takes an award type, applies it to the activites data
    Returns true if the award occured
    """
    print "Checking " + award.name

    # Force set date for testing
    award.set_now(now_date)

    print "Award time range: " + str(award.getStartDate()) + " to " + str(award.getEndDate())
    print arrow.get(award.getStartDate()).humanize()

    return check_award_occured(award)
