import time
from datetime import datetime
class sqlite:
    headers        = ('Id','Host','User','Password','Data')
    headersCheck   = ('Id','Host','User','Password','Data','Status')
    createTables   = 'CREATE TABLE IF NOT EXISTS database_bot (id integer PRIMARY KEY AUTOINCREMENT, ipadress text, user text,datestamp text, password text)'
    selectAllBots  = 'SELECT id,ipadress,user,password,datestamp FROM database_bot'
    deleteforID     = 'DELETE FROM database_bot WHERE id= {}'
    zeraids         = 'UPDATE SQLITE_SEQUENCE set seq=0 WHERE name="database_bot"'
def DB_insert(con,db,ipadress,user,password):
    data_time = str(datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))
    db.execute('INSERT INTO database_bot (ipadress,user,datestamp,password) VALUES(?,?,?,?)',(ipadress,user,data_time,password))
    con.commit()
def lengthDB(db):
    size = db.execute('SELECT * FROM database_bot')
    return len(size.fetchall())

def deleteID(con,db,id):
    db.execute(sqlite.deleteforID.format(str(id)))
    con.commit()