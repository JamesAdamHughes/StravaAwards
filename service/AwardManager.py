import arrow
from StravaAwards.model.DistanceAward import DistanceAward
from StravaAwards.model.ConsistancyAward import ConsistancyAward
from StravaAwards.service import emailUtilities, DatabaseManager

def check_award_occured(award, user_id, onlyNew):
    """
    Runs the award logic for an award, to test if it has occured
    Currently only works with SQL statements and consistancy awards
    """
    occured = award.check_occured()

    # check if the required no of acvities exist, 
    # Also check if the same award has already been given
    if onlyNew:
        previous_awards = get_award_from_db(award, user_id)
        print "[awardM] previous_awards" + str(previous_awards)

    if occured and previous_awards == []:
        print "[awardM] awarding user!"
        return True

    if previous_awards:
        print "[awardM] found old rewards, NOT REWARDING" + str(previous_awards)    

    return False


def get_award_from_db(award, user_id):
    """
    Returns an award from the database, using the start end and type as a unique identifier
    """

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

    params = [award.getStartDate(), award.getEndDate(), award.getAwardType(), user_id, award.name]
    result = DatabaseManager.fetch_one(sql, params)

    print "[awardM] fetched award: " + str(result)

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

    params = [user_id, award.name, award.getStartDate(), award.getEndDate(), award.getAwardType(), arrow.now().format()]
    DatabaseManager.insert_db(sql, params)

    return


def createAwards():
    """
    Return a list of strava award types
    """
    awards = []
    # todo write this up in json and read from file
    awards.append(ConsistancyAward('TwiceThisWeekAward', 0, 1, 0, 'You ran twice this week!', 1, 2, 0))
    awards.append(ConsistancyAward('Once This Week', 0, 1, 0, 'You ran once this week!', 1, 1, 0))
    awards.append(ConsistancyAward('TwoWeeksInARow', 0, 2, 0, 'You ran two weeks in a row!', 2, 1, 0))
    awards.append(ConsistancyAward('Four times a Month', 0, 0, 1, 'You ran four times this month!', 4, 1, 0))
    # awards.append(ConsistancyAward('Quadrupal threat', 0, 1, 0, 'You ran four times this month!', 1, 4, 0))
    awards.append(DistanceAward('Warm up', 0, 1, 0, 'You ran 5k this week!',5000 ,0))

    return awards

def get_new_awards_for_user(user_id, now_date, onlyNew=True):
    """
    Takes an award type, applies it to the activites data
    Returns true if the award occured
    """
    valid_awards = []
    for award in createAwards():
        # Force set date for testing
        award.set_now(now_date)

        print "[awardM] Checking " + award.name + " from " + arrow.get(award.getStartDate()).humanize()
        print "[awardM] date range is: " + award.getStartDate() + " to " + award.getEndDate()

        # Check if the award happened
        occured = check_award_occured(award, user_id, onlyNew)
        if occured:
            # save award to db
            valid_awards.append(award)
            save_award(award, user_id)
            print "[awardM] awarding: " + award.getAwardText()
    return valid_awards

