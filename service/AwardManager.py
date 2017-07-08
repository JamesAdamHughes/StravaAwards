import sqlite3

DBNAME = 'main.db'

def checkAwardOccured(award):

    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    # select from the database as needed
    awardSql = award.awardLogic()

    c.execute(awardSql)

    # Probably should pt this in the award object itself
    result = c.fetchone()
      
    conn.commit()
    conn.close()

    if result[0] == award.requiredActivites:
        return True
    else:
        return False
