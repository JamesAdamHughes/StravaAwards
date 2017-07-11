import sqlite3
from StravaConsistancyAward import StravaConsistancyAward
import arrow
from StravaAwards.service import emailUtilities

DBNAME = 'main.db'

def check_award_occured(award, user_id, onlyNew):
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
    activites = c.fetchone()

    conn.commit()
    conn.close()

    # check if the required no of acvities exist, 
    # Also check if the same award has already been given
    previous_awards = None
    if onlyNew:
        previous_awards = get_award_from_db(award, user_id)
        print "[awardM] previous_awards" + str(previous_awards)

    if activites[0] == award.requiredActivites:
        if previous_awards is None:
            print "[awardM] awarding user!"
            return True
        else:
            print "[awardM] found existing award " + str(previous_awards)
    else:
        print "[awardM] not enough activities" + str(activites)
    
    return False


def get_award_from_db(award, user_id):
    """
    Returns an award from the database, using the start end and type as a unique identifier
    """
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    sql = """
    select * 
    from tb_award
    where 1=1
        and datetime_start = ?
        and datetime_end = ?
        and type_id = ?
        and fk_user_id = ?
        and name = ?
        ;
    """
    c.execute(sql, [award.getStartDate(), award.getEndDate(), award.getAwardType(), user_id, award.name])
    result = c.fetchone()

    print "[awardM] fetched award: " + str(result)

    conn.commit()
    conn.close()
    return result


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

    c.execute(sql, [user_id, award.name, award.getStartDate(), award.getEndDate(), award.getAwardType(), arrow.now().format()])  

    conn.commit()
    conn.close() 
    return


def createAwards():
    """
    Return a list of strava award types
    """
    awards = []
    # todo write this up in json and read from file
    awards.append(StravaConsistancyAward('TwiceThisWeekAward', 0, 1, 0, 'You ran twice this week!', 1, 2, 0))
    awards.append(StravaConsistancyAward('Once This Week', 0, 1, 0, 'You ran once this week!', 1, 1, 0))
    # awards.append(StravaConsistancyAward('TwoWeeksInARow', 0, 2, 0, 'You ran two weeks in a row!', 2, 0))
    # awards.append(StravaConsistancyAward('Four times a Month', 0, 0, 1, 'You ran four times this month!', 4, 0))

    return awards

def get_new_awards_for_user(user_id, now_date, onlyNew=True):
    """
    Takes an award type, applies it to the activites data
    Returns true if the award occured
    """
    valid_awards = []
    
    print now_date

    for award in createAwards():
        # Force set date for testing
        award.set_now(now_date)

        print "[awardM] Checking " + award.name + " from " + arrow.get(award.getStartDate()).humanize()
        print award.getStartDate()

        # Check if the award happened
        occured = check_award_occured(award, user_id, onlyNew)
        if occured:
            # save award to db, send email
            valid_awards.append(award)
            save_award(award, user_id)
            print "[awardM] awarding: " + award.getAwardText()
    return valid_awards

