import arrow
from flask import current_app
from StravaAwards.model.DistanceAward import DistanceAward
from StravaAwards.model.ConsistancyAward import ConsistancyAward
from StravaAwards.service import emailUtilities, DatabaseManager, UserManager 

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

    return result


def save_award(award, user_id):
    """
    Takes an award and saves to to the db
    """
    log("saving award: " + str(award.name))
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


def create_awards():
    """
    Return a list of strava award types
    """
    awards = []
    # todo write this up in json and read from file
    awards.append(ConsistancyAward('Testing Triplet', 0, 1, 0, 'You ran three times this week!', 1, 3, 0))
    awards.append(ConsistancyAward('Double Tap', 0, 1, 0, 'You ran twice this week!', 1, 2, 0))
    awards.append(ConsistancyAward('Sweet Start', 0, 1, 0, 'You ran once this week!', 1, 1, 0))
    awards.append(ConsistancyAward('Fortnight Fighter', 0, 2, 0, 'You ran two weeks in a row!', 2, 1, 0))
    awards.append(ConsistancyAward('Monster Month', 0, 4, 0, 'You ran four weeks in a row!', 4, 1, 0))
    awards.append(ConsistancyAward('Quadrupal threat', 0, 0, 1, 'You ran four times this month!', 4, 1, 0))

    awards.append(DistanceAward('Warm up', 0, 1, 0, 'You ran 5k this week!',5000 ,0))
    awards.append(DistanceAward('Around the Block', 0, 1, 0, 'You ran 10k this week!',10000 ,0))
    awards.append(DistanceAward('Almost a Half!', 0, 1, 0, 'You ran 15k this week!',20000 ,0))

    return awards

def get_new_awards_for_user(user_id, now_date, onlyNew=True):
    ''' Takes an award type, applies it to the activites data
    Returns true if the award occured

    :param user_id: int ID of user to be rewarded
    '''
    valid_awards = []
    for award in create_awards():
        # Force set date for testing
        award.set_now(now_date)

        log("Checking " + award.name + " date range is: " + award.getStartDate() + " to " + award.getEndDate())

        # Check if the award happened
        occured = award.check_occured(user_id)

        #check if we have already given the award out (already met conditions once)
        previous_awards = get_award_from_db(award, user_id)
        log("previous_awards" + str(previous_awards))
        
        if previous_awards and onlyNew:
            # already given award and are only looking for new ones
            log("found old rewards, NOT REWARDING" + str(previous_awards)) 

        elif occured and (previous_awards == [] or not onlyNew):
            # award conditions met and we haven't given before or forcing new
            log("awarding: " + award.getAwardText())

            # save award to db
            valid_awards.append(award)
            save_award(award, user_id)
            log("awarding: " + award.getAwardText())

    return valid_awards


def award_user(user_id, awards):
    """
    Given a user id and a list of awards, 
    Send an email to the user containing all awards they recieved
    """

    user = UserManager.get_user(user_id)
    if not user:
        return False

    subject = "Congrats {0}, You won {1} Strava awards!".format(user.f_name, len(awards))

    award_text_list = "<ul>"
    for award in awards:
        log(award.name)
        award_item = "<li>" + award.get_html_template() + "</li>"
        award_text_list += award_item

    award_text_list += "</ul>"

    sent = emailUtilities.send_email(subject, award_text_list)

    return sent

def log(text):
    current_app.logger.info("[awardManager]: " + str(text))
