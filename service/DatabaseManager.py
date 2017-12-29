from StravaAwards import definitions
import sqlite3

DBNAME = definitions.ROOT_DIR +  '/main.db'

def get_db_ccursor():
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    return c, conn

def insert_db(sql, params):
    c, conn = get_db_ccursor()

    if params:
        result = c.execute(sql, params)
    else:
        result = c.execute(sql)

    close_connection(conn)
    return result

def close_connection(conn):
    conn.commit()
    conn.close()

def fetch_one(sql, params=None):
    c, conn = get_db_ccursor()

    if params:
        c.execute(sql, params)
    else:
        c.execute(sql)

    # Get column names
    names = [description[0] for description in c.description]

    # Get results from the db
    # Map each column in the row, to the associated column name
    results = []
    row = c.fetchone()
    if row:
        results.append(dict(zip(names, row)))

    close_connection(conn)

    return results

def fetch_all(sql, params=None):
    c, conn = get_db_ccursor()

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

    close_connection(conn)

    return results
