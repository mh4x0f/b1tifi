#!/usr/bin/env python2.7
from os import path,mkdir
from shell.core.main import Console
from shell.core.utility.color import banner
version = '1.3.2'
author  = 'Marcos Nesster (@mh4x0f)'
def main():
    folderDB = path.expanduser('~/.b1tifi-db')
    db_path = path.join(folderDB, 'b1tifi.db')
    if not path.exists(folderDB):
        mkdir(folderDB)
    shell = Console(db_path)
    shell.cmdloop(banner(version,author))
