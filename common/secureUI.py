#The MIT License (MIT)
#Version 1.1
#Copyright (c) 2014 Marcos Nesster (mh4x0f)
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import pxssh
import time
from helpers.color import setcolor,display_messages
import signal
import threading
from utils import Thread_Jobs
from datetime import datetime
class ssh(object):
    def __init__(self, host,port, user, password,checkconnect=True):
        self.settings   = {'Host': host,'User': user,'Port': port,'Password': password}
        self.jobs       = {'Running': False,'Command': None,'Packets':[]}
        self.connection,self.password = checkconnect,password
        self.status,self.session,self.on = None,None,False
        thread_connect  = threading.Thread(target=self.ThreadSSH,args=[])
        thread_connect.setDaemon(True)
        thread_connect.start()
        thread_connect.join()

    def job_start(self,cmd):
        self.thread_jobs  = Thread_Jobs(cmd,self.session)
        self.thread_jobs.setDaemon(True)
        self.thread_jobs.start()
        self.jobs['Running'] = True
        self.jobs['Command'] = cmd
        display_messages('Started Job::{} from command:: {}'.format(self.settings['Host'],cmd),sucess=True)
        self.jobs['Packets'] = [self.settings['Host'],self.jobs['Command'],
        str(datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))]

    def job_stop(self):
        self.thread_jobs.stop(self.settings['Host'])
        self.jobs['Running'] = False

    def ThreadSSH(self):
        try:
            self.session = pxssh.pxssh()
            self.session.login(self.settings['Host'], self.settings['User'],
            self.settings['Password'],port=self.settings['Port'])
            if self.connection:
                self.status = '[{}]'.format(setcolor('ON',color='green'))
                self.on = True
        except Exception, e:
            self.status = '[{}]'.format(setcolor('OFF',color='red'))
            self.on = False

    def logout(self):
        self.session.terminate(True)

    def info(self):
        print display_messages('System Informations:',sublime=True,info=True)
        print('Host     :: {}'.format(self.settings['Host']))
        print('PID      :: {}'.format(self.session.pid))
        print('timeout  :: {}'.format(self.session.timeout))
        print('Shell    :: {}'.format(self.session.name))
        kernelversion = self.send_command('uname -r')
        print('Kernel   :: {}\n'.format(kernelversion.split()))

    def interactive(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        print display_messages('Remote Shell:',sublime=True,info=True)
        self.session.PROMPT_SET_SH = "PS1='{}@{}\$ '".format(self.settings['Host'],self.settings['User'])
        self.session.auto_prompt_reset = False
        self.session.set_unique_prompt()
        self.session.interact()
        print display_messages('Session closed {}'.format(self.session.name),info=True)

    def signal_handler(self,signal, frame):
        print('Exit interact shell!')
        self.session.terminate(True)
    def send_command(self,cmd):
        self.session.sendline(cmd)
        try:
            self.session.prompt()
            return str(self.session.before).replace(cmd,'')
        except Exception : return ''