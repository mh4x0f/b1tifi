#!/usr/bin/env python2.7
from os import path,mkdir
from shell.core.consoleUI import Console
from shell.core.utils.color import banner
version = '1.3.2'
author  = 'Marcos Nesster (@mh4x0f)'
def main():
    folderDB = path.expanduser('~/.botdr4g0n-db')
    db_path = path.join(folderDB, 'botdr4g0n.db')
    if not path.exists(folderDB):
        mkdir(folderDB)
    shell = Console(db_path)
    shell.cmdloop(banner(version,author))
