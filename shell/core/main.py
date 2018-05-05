import sqlite3
import shell.core.connection.ssh as SSHConnection
from shell.core.common.console import ConsoleUI
import shell.core.utility.constants as C

class Console(ConsoleUI):
    ''' main class console UI'''
    def __init__(self,path):
        self.load_database(path)
        self.ssh        = SSHConnection
        self.settings   = {'all' :{},'check' :[],'agents':{}}
        ConsoleUI.__init__(self,self.settings,self.ssh, {'db_con': self.con, 'db_cursor': self.db})

    def load_database(self, path):
        self.con    = sqlite3.connect(path)
        self.db     = self.con.cursor()
        self.db.execute(C.createTables)

    def do_modules(self, args):
        ''' show all modules '''
        pass

    def precmd(self, line):
        newline=line.strip()
        is_cmt=newline.startswith('#')
        if is_cmt:
            return ('')
        return (line)

    def postcmd(self, stop, line):
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass