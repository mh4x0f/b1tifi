import threading
from shell.core.utility.color import display_messages
class Thread_Jobs(threading.Thread):
    def __init__(self,cmd,session):
        threading.Thread.__init__(self)
        self.session = session
        self.command = cmd

    def run(self):
        self.session.sendline(self.command)
        self.session.prompt()

    def stop(self,host):
        display_messages('Jobs:{} Stoped Command:: {}'
        .format(host,self.command),error=True)
        self.session.close()