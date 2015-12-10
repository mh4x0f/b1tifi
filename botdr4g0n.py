#!/usr/bin/env python2.7
from common.ConsoleUI import Console
from helpers.color import banner
version = '0.1.3'
author  = 'Marcos Nesster (@mh4x0f)'
if __name__ == '__main__':
    shell = Console()
    shell.cmdloop(banner(version,author))
