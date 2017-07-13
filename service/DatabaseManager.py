from StravaAwards import definitions

DBNAME = definitions.ROOT_DIR +  '/main.db'
print '[activityM] root dir: ' + DBNAME

def getDbCCursor():
    print 'dbname: ' + DBNAME
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    return c, conn

def insertDb(sql, params):
    c, conn = getDbCCursor()

    if params:
        c.execute(sql, params)
    else :
        c.execute(sql)
   
    closeConnection(conn)
    return

def closeConnection(conn):
    conn.commit()
    conn.close()

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