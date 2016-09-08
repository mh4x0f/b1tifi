#The MIT License (MIT)
#Copyright (c) 2014-2016 Marcos Nesster (mh4x0f)
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
import argparse
import cmd
import shlex
import sqlite3
from os import system,path,getcwd
from subprocess import check_output
from re import search
from tabulate import tabulate
import shell.core.libs.secureSSH as SSHConnection
from shell.core.utils import color,funcSQL
class Console(cmd.Cmd):
    def __init__(self,db_path):
        cmd.Cmd.__init__(self)
        self.prompt = color.setcolor(':: ', color='Blue')
        self.con    = sqlite3.connect(db_path)
        self.db     = self.con.cursor()
        self.db.execute(funcSQL.sqlite.createTables)
        self.settings   = {'all' :{},'check' :[],'agents':{}}
        self.sshConnect = SSHConnection
        self.search_all_agents()

    def do_list(self,args):
        """ list/check/filter list agents on database """
        arg_parser = argparse.ArgumentParser(prog='list',description='interact with one/all agents')
        arg_parser.add_argument('-i', '--id', dest='id',type=int,metavar='<id>', help='list agent  by id')
        arg_parser.add_argument('-c', '--check',dest='check', action='store_true', help='check credentials by agent Available')
        arg_parser.add_argument('-d', '--db',dest='database', action='store_true', help='list all agents on database')
        try:
            args=arg_parser.parse_args(shlex.split(args))
        except: return
        self.settings['all'] = {}
        self.listbotsprint = []
        for agent in self.db.execute(funcSQL.sqlite.selectAllBots):self.settings['all'][agent[0]] = agent
        if self.settings['all'] == {}:
            return color.display_messages('No Agents registered',info=True)
        if args.database:
            if args.id and not args.check:
                if not args.id in self.settings['all'].keys():
                    return color.display_messages('ID not registered',info=True)
                color.display_messages('Agents:', info=True, sublime=True)
                agent = list(self.settings['all'][args.id])
                self.listbotsprint += list([agent])
                print tabulate(self.listbotsprint, headers=funcSQL.sqlite.headersCheck)

            elif args.check and args.id:
                if not args.id in self.settings['all'].keys():
                    return color.display_messages('ID not registered', info=True)
                color.display_messages('Agents:', info=True, sublime=True)
                agent = list(self.settings['all'][args.id])
                agent.insert(len(agent),self.sshConnect.ssh(agent[1],agent[2],agent[3],agent[4],checkconnect=True).status)
                self.listbotsprint += list([agent])
                print tabulate(self.listbotsprint, headers=funcSQL.sqlite.headersCheck)


            elif args.database and not args.check:
                color.display_messages('Agents:', info=True, sublime=True)
                for bots in self.settings['all'].items():self.listbotsprint += list([bots[1]])
                print tabulate(self.listbotsprint, headers=funcSQL.sqlite.headers)
                return color.linefeed()

            elif args.database and not args.id:
                color.display_messages('Agents:', info=True, sublime=True)
                for agent in self.settings['all'].items():
                    agent = list(agent[1])
                    agent.insert(len(agent),self.sshConnect.ssh(agent[1],agent[2],agent[3],agent[4],checkconnect=True).status)
                    self.listbotsprint += list([agent])
                print tabulate(self.listbotsprint, headers=funcSQL.sqlite.headersCheck)
                color.linefeed()
        else:
            arg_parser.print_help()

    def do_jobs(self,args):
        """ list/kill jobs running on agents """
        arg_parser = argparse.ArgumentParser(prog='jobs',description='list/kill jobs running on agents')
        arg_parser.add_argument('-i', '--id', dest='id',type=int,metavar='<id>', help='kill agent by id')
        arg_parser.add_argument('-k', '--kill',dest='kill', action='store_true', help='kill jobs by id/all')
        arg_parser.add_argument('-l', '--list',dest='list', action='store_true', help='list all jobs')
        try:
            args=arg_parser.parse_args(shlex.split(args))
        except: return
        self.settings['all'] = {}
        jobs = []
        for agent in self.db.execute(funcSQL.sqlite.selectAllBots):self.settings['all'][agent[0]] = agent
        if self.settings['all'] == {}:
            return color.display_messages('No Agents registered', info=True)
        if args.list:
            for agent in self.settings['agents'].keys():
                if self.settings['agents'][int(agent)]['tunel'] != None:
                    if  self.settings['agents'][int(agent)]['tunel'].jobs['Running']:
                        color.display_messages('Jobs:', info=True, sublime=True)
                        listjobs = self.settings['agents'][int(agent)]['tunel'].jobs['Packets']
                        listjobs.insert(0,int(agent))
                        jobs.append(listjobs)
            if jobs != []:
                print tabulate(jobs, headers=funcSQL.sqlite.headersJobs)
                return
            color.display_messages('not command jobs activated', info=True)

        elif args.id and args.kill:
            if args.id in self.settings['agents'].keys():
                if self.settings['agents'][args.id]['tunel'] != None:
                    return self.settings['agents'][args.id]['tunel'].job_stop()
            color.display_messages('Job:: From Id {} not found'.format(args.id), info=True)

        elif args.kill:
            for agent in self.settings['agents'].keys():
                if self.settings['agents'][int(agent)]['tunel'] != None:
                    self.settings['agents'][int(agent)]['tunel'].job_stop()
        else:
            arg_parser.print_help()

    def do_agents(self,args):
        """ list all agents in interacting """
        list_agents = []
        # get all session activated
        if self.settings['agents'].keys() != {}:
            for agent in self.settings['agents'].keys():
                if self.settings['agents'][agent]['tunel'] != None:
                    if self.settings['agents'][agent]['tunel'].activated:
                        list_agents.append([agent,self.settings['agents'][agent]['creds']['Host'],
                self.settings['agents'][agent]['creds']['Port'],
                    self.settings['agents'][agent]['tunel'].session.name,
                        self.settings['agents'][agent]['tunel'].session.pid])
            if list_agents != []:
                color.display_messages('Session Agents:', info=True, sublime=True)
                print tabulate(list_agents,headers=funcSQL.sqlite.headersAgents)
                color.linefeed()
                return color.display_messages('Online Agents: {}'.format(color.setcolor(str(len(list_agents)),
                color='blue')), info=True)
        color.display_messages('No agents in interacting', info=True)

    def do_interact(self,args):
        """ interact with one/all agents """
        arg_parser = argparse.ArgumentParser(prog='interact',description='interact with one/all agents')
        arg_parser.add_argument('-i', '--id', dest='id',type=int,metavar='<id>', help='connect with particular agent SSH by id')
        arg_parser.add_argument('-a', '--all',dest='all', action='store_true', help='connect all agent Available')
        arg_parser.add_argument('-s', '--shell',dest='shell', action='store_true', help='connect Remote shell bin/bash')
        arg_parser.add_argument('-q', '--quit',dest='quit', action='store_true', help='quit all connections with agents')
        try:
            args=arg_parser.parse_args(shlex.split(args))
        except: return
        if args.id and not args.quit:
            self.search_on_agents()
            if args.id in self.settings['agents'].keys():
                if args.shell: return self.interactive_binbash(args.id) # call shell interactive /bin/bash
                # connect client ssh
                self.settings['agents'][args.id]['tunel'] = self.sshConnect.ssh(
                self.settings['agents'][args.id]['creds']['Host'],
                self.settings['agents'][args.id]['creds']['Port'],
                self.settings['agents'][args.id]['creds']['User'],
                self.settings['agents'][args.id]['creds']['Pass'])
                return color.display_messages('Agent added:: {}:{} status::[{}]'.format(
                self.settings['agents'][args.id]['creds']['Host'],
                self.settings['agents'][args.id]['creds']['Port'],
                color.setcolor('Ok', color='green')),info=True)
            color.display_messages('ID: could not be found', error=True)

        elif args.id and args.quit:
            # desconnect agents from ID
            if args.id in self.settings['agents'].keys():
                if self.settings['agents'][args.id]['tunel'] != None:
                    if self.settings['agents'][args.id]['tunel'].activated:
                        color.display_messages('HOST::{}:{} broken::[{}]'.format(
                        self.settings['agents'][args.id]['creds']['Host'],
                        self.settings['agents'][args.id]['creds']['Port'],
                        color.setcolor('OFF', color='red')), info=True)
                        return self.settings['agents'][args.id]['tunel'].logout()
            color.display_messages('ID: could not be found', error=True)

        elif args.all:
            # connect all agents
            self.search_on_agents()
            if self.settings['agents'].keys() == []:
                return color.display_messages('No agents for kill sessions', error=True)
            for agent in self.settings['agents'].keys():
                self.settings['agents'][agent]['tunel'] = self.sshConnect.ssh(
                self.settings['agents'][agent]['creds']['Host'],
                self.settings['agents'][agent]['creds']['Port'],
                self.settings['agents'][agent]['creds']['User'],
                self.settings['agents'][agent]['creds']['Pass'])
                color.display_messages('Agent:: {}:{} status::[{}]'.format(
                self.settings['agents'][agent]['creds']['Host'],
                self.settings['agents'][agent]['creds']['Port'],
                color.setcolor('Ok', color='green')),info=True)

        elif args.quit:
            # kill all connection activated
            listAgents = []
            self.search_on_agents()
            if self.settings['agents'].keys() == []:
                return color.display_messages('No Agents registered', error=True)
            for agent in self.settings['agents'].keys():
                if self.settings['agents'][int(agent)]['tunel'] != None:
                    color.display_messages('HOST::{}:{} broken::[{}]'.format(
                    self.settings['agents'][agent]['creds']['Host'],
                    self.settings['agents'][agent]['creds']['Port'],
                    color.setcolor('OFF', color='red')), info=True)
                    self.settings['agents'][int(agent)]['tunel'].logout()
                    listAgents.append(agent)
            if listAgents != []:
                return color.display_messages('Connection broken all agents', info=True)
            color.display_messages('No agents for kill session', error=True)

        else:
            arg_parser.print_help()

    def do_execute(self,args):
        """ execute command on agents"""
        arg_parser = argparse.ArgumentParser(prog='execute',description="execute command's on agents")
        arg_parser.add_argument('-c', '--cmd',dest='cmd',metavar='"cmd"', help='execute command on bot')
        arg_parser.add_argument('-j', '--job',dest='jobs', action='store_true', help='running command as job')
        try:
            args=arg_parser.parse_args(shlex.split(args))
        except: return
        if args.cmd and not args.jobs:
            for agent in self.settings['agents'].keys():
                if self.settings['agents'][int(agent)]['tunel']:
                    if not self.settings['agents'][int(agent)]['tunel'].jobs['Running']:
                        if self.settings['agents'][agent]['tunel'].activated:
                            color.display_messages('HOST::{}'.format(self.settings['agents']
                            [agent]['creds']['Host']), info=True, sublime=True)
                            self.stdout.write(self.settings['agents'][agent]['tunel'].send_command(args.cmd))
                    else:
                        color.display_messages('Status: Unable to process request,'
                        ' agent:: [{}] is busy in Jobs'.format(
                        self.settings['agents'][agent]['creds']['Host']),error=True)
        elif args.cmd and args.jobs:
            for agent in self.settings['agents'].keys():
                if self.settings['agents'][int(agent)]['tunel'].activated:
                    self.settings['agents'][int(agent)]['tunel'].job_start(args.cmd)
        else:
            arg_parser.print_help()

    def do_sysinfo(self,args):
        """ print information session on agents"""
        for agent in self.settings['agents'].keys():
            if self.settings['agents'][int(agent)]['tunel']:
                self.stdout.write(str(self.settings['agents'][int(agent)]['tunel'].info()))

    def interactive_binbash(self,id):
        self.stdout.write(str(self.settings['agents'][id]['tunel'].interactive()))

    def do_check(self,args):
        """ test all agents login ssh  """
        agentsCount = 0
        self.settings['check'] = []
        for agent in self.db.execute(funcSQL.sqlite.selectAllBots):
            agent = list(agent)
            agent.insert(len(agent),self.sshConnect.ssh(agent[1],agent[2],agent[3],agent[4],checkconnect=True).status)
            self.settings['check'].append(agent)
        color.display_messages('Available Bots:', info=True, sublime=True)
        print tabulate(self.settings['check'], headers=funcSQL.sqlite.headersCheck)
        for items in self.settings['check']:
            if search('ON',items[6]):agentsCount +=1
        color.linefeed()
        color.display_messages('Online Agents: {}'.format(color.setcolor(str(agentsCount), color='blue')), info=True)

    def search_all_agents(self):
        for agent in self.db.execute(funcSQL.sqlite.selectAllBots):self.settings['all'][agent[0]] = agent

    def search_on_agents(self):
        for agent in self.db.execute(funcSQL.sqlite.selectAllBots):
            if not agent[0] in self.settings['agents'].keys():
                self.settings['agents'][agent[0]] = {'creds':{},'tunel':None}
                self.settings['agents'][agent[0]]['creds']['ID']   = agent[0]
                self.settings['agents'][agent[0]]['creds']['Host'] = agent[1]
                self.settings['agents'][agent[0]]['creds']['Port'] = agent[2]
                self.settings['agents'][agent[0]]['creds']['User'] = agent[3]
                self.settings['agents'][agent[0]]['creds']['Pass'] = agent[4]

    def do_register(self,args):
        """ add bot on database """
        arg_parser = argparse.ArgumentParser(prog='register',description='add bot on database clients')
        arg_parser.add_argument('--host', dest='host',metavar='<Host>', help='ipaddress/host/dns connect ssh')
        arg_parser.add_argument('--pass', dest='password',metavar='<Password>', help='password ssh client')
        arg_parser.add_argument('-u', '--user',dest='user', metavar='<user>', help='delete all bot registered')
        arg_parser.add_argument('-p', '--port', dest='port',metavar='<Port>',default='22', help='port connect ssh')
        arg_parser.add_argument('-f', '--file', dest='file',metavar='<filepath>', help='imports clients from a file')
        try:
            args=arg_parser.parse_args(shlex.split(args))
        except: return
        if args.host and args.password and args.user:
            color.display_messages('Insert Data: SQL statement will insert a new row', info=True)
            funcSQL.DB_insert(self.con, self.db, args.host, args.port, args.user, args.password)
            color.display_messages('credentials ssh added with success', sucess=True)
        elif args.file:
            self.all_bot_checked = []
            color.display_messages('searching for: {} ...'.format(path.realpath(args.file)),info=True)
            if path.exists(args.file):
                self.lines_all_read = [line.rstrip('\n') for line in open(path.realpath(args.file),'r')]
                for items in self.lines_all_read:
                    if len(items.split()) == 4:
                        self.all_bot_checked.append(items)
                if len(self.all_bot_checked) == 0:
                    color.display_messages('Instruction for -f argumments:',info=True,sublime=True)
                    print('You need to use the separator character [space] in this format below\n')
                    print('-----cut here -------\n')
                    print('root:~# cat example.txt\n')
                    print('192.168.0.100 22 DemoBOT P@ssW0rd')
                    print('192.168.0.120 22 Userdr4g0n botP@ssW0rd')
                    print('\n-----cut here -------\n')
                    print('')
                    return None
                self.ListBot = []
                color.display_messages('All agents imported from file:', info=True,sublime=True)
                for agent in self.all_bot_checked: self.ListBot += list([agent.split()])
                print tabulate(self.ListBot, headers=funcSQL.sqlite.headersimport)
                color.linefeed()
                choise = raw_input('{}[*]{} Do you want to import?(S/N):'.format(color.colors.GREEN,color.colors.ENDC,))
                if choise.lower() == 's':
                    color.display_messages('Importing agents...',info=True)
                    for agent  in self.all_bot_checked:
                        funcSQL.DB_insert(self.con, self.db,
                            agent.split()[0],agent.split()[1],agent.split()[2],agent.split()[3])
                    return color.display_messages('all agents ssh added with success', sucess=True)
                color.display_messages('import was been canceled.', error=True)
            else:
                color.display_messages('file: could not be found', error=True)
        else:
            arg_parser.print_help()

    def do_del(self,args):
        """ delete bot using <id>/all """
        arg_parser = argparse.ArgumentParser(prog='del',description='delete an bot registered')
        arg_parser.add_argument('-i', '--id', dest='id',metavar='<id>',type=int, help='delete by ID bot')
        arg_parser.add_argument('-a', '--all',dest='all', action='store_true', help='delete all bot registered')
        try:
            args=arg_parser.parse_args(shlex.split(args))
        except: return
        if args.id:
            self.search_all_agents()
            if not args.id in self.settings['all'].keys():
                color.display_messages('ID not found', info=True)
                return
            items =  self.settings['all'][args.id]
            color.display_messages('Found ID:', sublime=True, info=True)
            color.display_messages('Search query for finding a particular id', info=True)
            color.display_messages('Section DELETE FROM statement.', info=True)
            color.display_messages('ID:{} Host:{} Port:{} User:{} Password:{})'.format(items[0], items[1], items[2], items[3], items[4]), info=True)
            funcSQL.deleteID(self.con, self.db, args.id)
            if funcSQL.lengthDB(self.db) < 1:
                self.db.execute(funcSQL.sqlite.zeraids)
                self.con.commit()
        elif args.all:
            self.db.execute(funcSQL.sqlite.delete_all)
            self.db.execute(funcSQL.sqlite.createTables)
            color.display_messages('All data has been removed.',info=True)
            self.con.commit()
        else:
            arg_parser.print_help()

    def update(self):
        self.con.commit()

    def do_help(self,args):
        """ show this help """
        names = self.get_names()
        cmds_doc = []
        names.sort()
        pname = ''
        color.display_messages('Available Commands:', info=True, sublime=True)
        for name in names:
            if name[:3] == 'do_':
                pname = name
                cmd   = name[3:]
                if getattr(self, name).__doc__:
                    cmds_doc.append((cmd, getattr(self, name).__doc__))
                else:
                    cmds_doc.append((cmd, ""))

        #self.stdout.write('%s\n'%str(self.doc_header))
        self.stdout.write('    {}	 {}\n'.format('Commands', 'Description'))
        self.stdout.write('    {}	 {}\n'.format('--------', '-----------'))
        for command,doc in cmds_doc:
            self.stdout.write('    {:<10}	{}\n'.format(command, doc))
        color.linefeed()

    def do_clear(self,args):
        """ clean up the line """
        system('clear')

    def do_update(self,args):
        """ find newer versions """
        color.display_messages('checking updates...', info=True)
        color.display_messages(check_output(['git', 'pull']), info=True)

    def default(self, args):pass
    def emptyline(self):pass

    def do_exit(self, args):
        """ exit the program."""
        print "Quitting."
        raise SystemExit