#!/usr/bin/env python2.7
from common.ConsoleUI import Console
from helpers.color import banner
if __name__ == '__main__':
    shell = Console()
    shell.cmdloop(banner())
