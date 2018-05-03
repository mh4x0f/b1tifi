import time
from datetime import datetime

headers        = ('Id','Host','Port','User','Password/key','Data')
headersimport  = ('Host','Port','User','Password/key','Data')
headersCheck   = ('Id','Host','Port','User','Password/key','Data','Status')
headersJobs    = ('Id','Host','Running','Start Data')
headersAgents  = ('Id','Host','Port','Shell','Process')
createTables   = 'CREATE TABLE IF NOT EXISTS database_bot (id integer PRIMARY KEY AUTOINCREMENT, ipadress text,port text, user text,datestamp text, password text)'
selectAllBots  = 'SELECT id,ipadress,port,user,password,datestamp FROM database_bot'
deleteforID     = 'DELETE FROM database_bot WHERE id= {}'
zeraids         = 'UPDATE SQLITE_SEQUENCE set seq=0 WHERE name="database_bot"'
delete_all      = 'DROP TABLE IF EXISTS database_bot'



def DB_insert(con,db,ipadress,port,user,password):
    data_time = str(datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))
    db.execute('INSERT INTO database_bot (ipadress,port,user,datestamp,password) VALUES(?,?,?,?,?)',(ipadress,port,user,data_time,password))
    con.commit()
def lengthDB(db):
    size = db.execute('SELECT * FROM database_bot')
    return len(size.fetchall())

def deleteID(con,db,id):
    db.execute(sqlite.deleteforID.format(str(id)))
    con.commit()
