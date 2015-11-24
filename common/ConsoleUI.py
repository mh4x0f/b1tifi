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
import cmd
import ssh
import shlex
import sqlite3
import argparse
from re import search
from helpers import color
from helpers import funcSQL
from tabulate import tabulate
class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = color.setcolor(':: ',color='Blue')
        self.con    = sqlite3.connect('helpers/database.db')
        self.db     = self.con.cursor()
        self.db.execute(funcSQL.sqlite.createTables)
        self.settings   = {'limited':None,'all' :[],'check' :[],'agents':{}}
        self.sshConnect = ssh
        self.search_all_agents()
    def do_list(self,args):
        """ list all bots in-database """
        self.settings['all'] = []
        for bot in self.db.execute(funcSQL.sqlite.selectAllBots):self.settings['all'].append(bot)
        if self.settings['all'] != []:
            print color.display_messages('Agents:',info=True,sublime=True)
            print tabulate(self.settings['all'],headers=funcSQL.sqlite.headers)
            color.linefeed()
            return
        print color.display_messages('No Agents registered',info=True)

    def do_interact(self,args):
        """ interact with one/all agents """
        arg_parser = argparse.ArgumentParser(prog='interact',description='interact with one/all agents')
        arg_parser.add_argument('-i', '--id', dest='id',type=int,metavar='<id>', help='connect with particular agent SSH by id')
        arg_parser.add_argument('-a', '--all',dest='all', action='store_true', help='connect all agent Available')
        arg_parser.add_argument('-r', '--reset',dest='reset', action='store_true', help='reset all connections with agents')
        try:
            args=arg_parser.parse_args(shlex.split(args))
        except: return
        if args.id:
            print color.display_messages('Checking Creadentials SHH...',info=True)
            self.search_on_agents()
            if args.id in self.settings['agents'].keys():
                print color.display_messages('connecting...',info=True)
                self.settings['agents'][args.id]['tunel'] = self.sshConnect.ssh(
                self.settings['agents'][args.id]['creds']['Host'],
                self.settings['agents'][args.id]['creds']['User'],
                self.settings['agents'][args.id]['creds']['Pass'])
                print color.display_messages('Agent::{} [{}]\n'.format(
                self.settings['agents'][args.id]['creds']['Host'],
                color.setcolor('ON',color='green')),info=True)
                self.settings['limited'] = args.id
            print color.display_messages('Added bot with success.',sucess=True)
        elif args.all:
            print color.display_messages('Checking Creadentials SHH...',info=True)
            self.search_on_agents()
            for agent in self.settings['agents'].keys():
                self.settings['agents'][agent]['tunel'] = self.sshConnect.ssh(
                self.settings['agents'][agent]['creds']['Host'],
                self.settings['agents'][agent]['creds']['User'],
                self.settings['agents'][agent]['creds']['Pass'])
                print color.display_messages('Agent::{} [{}]\n'.format(
                self.settings['agents'][agent]['creds']['Host'],
                color.setcolor('ON',color='green')),info=True)
            self.settings['limited'] = None
            print color.display_messages('Added botnets with success.',sucess=True)
        elif args.reset:
            self.search_on_agents()
            self.settings['limited'] = None
            print color.display_messages('Reseted all connections with agents',info=True)
        else:
            arg_parser.print_help()

    def do_shell(self,args):
        """ execute command on agents"""
        if args != '':
            if self.settings['limited'] != None:
                self.stdout.write(self.settings['agents'][self.settings['limited']]['tunel'].send_command(args))
                return
            else:
                for agent in self.settings['agents'].keys():
                    if self.settings['agents'][int(agent)]['tunel']:
                        print color.display_messages('HOST::{}'.format(self.settings['agents'][agent]['creds']['Host']),
                        info=True,sublime=True)
                        self.stdout.write(self.settings['agents'][int(agent)]['tunel'].send_command(args))
                        color.linefeed()
                return
        print color.display_messages('Usage: shell <cmd>',info=True)

    def do_check(self,args):
        """ test all agents login ssh  """
        agentsCount = 0
        self.settings['check'] = []
        for agent in self.db.execute(funcSQL.sqlite.selectAllBots):
            agent = list(agent)
            agent.insert(len(agent),self.sshConnect.ssh(agent[1],agent[2],agent[3],checkconnect=True).status)
            self.settings['check'].append(agent)
        print color.display_messages('Available Bots:',info=True,sublime=True)
        print tabulate(self.settings['check'],headers=funcSQL.sqlite.headersCheck)
        for items in self.settings['check']:
            if search('ON',items[5]):agentsCount +=1
        color.linefeed()
        print color.display_messages('Agents: {}'.format(color.setcolor(str(agentsCount),color='blue')),info=True)

    def search_all_agents(self):
        for bot in self.db.execute(funcSQL.sqlite.selectAllBots):self.settings['all'].append(bot)

    def search_on_agents(self):
        for agent in self.db.execute(funcSQL.sqlite.selectAllBots):
            if  (self.sshConnect.ssh(agent[1],agent[2],agent[3],checkconnect=True).on):
                self.settings['agents'][agent[0]] = {'creds':{},'tunel':None}
                self.settings['agents'][agent[0]]['creds']['ID']   = agent[0]
                self.settings['agents'][agent[0]]['creds']['Host'] = agent[1]
                self.settings['agents'][agent[0]]['creds']['User'] = agent[2]
                self.settings['agents'][agent[0]]['creds']['Pass'] = agent[3]

    def do_register(self,args):
        """ add bot on database """
        arg_parser = argparse.ArgumentParser(prog='register',description='add bot on database clients')
        arg_parser.add_argument('-i', '--ipaddress', dest='host',metavar='<Host>', help='ipaddress/host/dns connect ssh')
        arg_parser.add_argument('-p', '--password', dest='password',metavar='<Password>', help='password ssh client')
        arg_parser.add_argument('-u', '--user',dest='user', metavar='<user>', help='delete all bot registered')
        try:
            args=arg_parser.parse_args(shlex.split(args))
        except: return
        if args.host and args.password and args.user:
            print color.display_messages('Insert Data: SQL statement will insert a new row',info=True)
            funcSQL.DB_insert(self.con,self.db,args.host,args.user,args.password)
            print color.display_messages('credentials ssh added with success',sucess=True)
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
            for items in self.settings['all']:
                if int(items[0]) == args.id:
                    print color.display_messages('Search ID:',sublime=True,info=True)
                    print color.display_messages('Search query for finding a particular id',info=True)
                    print color.display_messages('Section DELETE FROM statement.',info=True)
                    print color.display_messages('ID:{} (Host:{} User:{} Password:{})'.format(items[0],items[1],items[2],items[3],items[4]),info=True)
                    funcSQL.deleteID(self.con,self.db,args.id)
            if funcSQL.lengthDB(self.db) < 1:
                self.db.execute(funcSQL.sqlite.zeraids)
                self.con.commit()
        elif args.all:
            for i in range(funcSQL.lengthDB(self.db)):
                funcSQL.deleteID(self.con,self.db,i)
            self.db.execute(funcSQL.sqlite.zeraids)
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
        print color.display_messages('Available Commands:',info=True,sublime=True)
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
        print('\n')

    def default(self, args):pass
    def emptyline(self):pass
    def do_exit(self, args):
        """ exit the program."""
        print "Quitting."
        raise SystemExit