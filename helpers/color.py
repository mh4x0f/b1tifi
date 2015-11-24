class colors:
    BOLD = '\033[1m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    CIANO = '\033[1m'
    ORAN= '\033[91m'
    GREY= '\033[37m'
    DARKGREY = '\033[1;30m'
    UNDERLINE = '\033[4m'

def setcolor(text,color=''):
    colorfinal = ''
    if   color.lower()=='blue':colorfinal=colors.BOLD+colors.BLUE+text+colors.ENDC
    elif color.lower()=='red':colorfinal=colors.BOLD+colors.RED+text+colors.ENDC
    elif color.lower()=='green':colorfinal=colors.BOLD+colors.GREEN+text+colors.ENDC
    elif color.lower()=='yellow':colorfinal=colors.BOLD+colors.YELLOW+text+colors.ENDC
    elif color.lower()=='grey':colorfinal=colors.BOLD+colors.GREY+text+colors.ENDC
    elif color.lower()=='darkgrey':colorfinal=colors.BOLD+colors.DARKGREY+text+colors.ENDC
    return colorfinal

def linefeed():
    print('\n')
def display_messages(string,error=False,sucess=False,info=False,sublime=False,without=False):
    if sublime:
        if   error:return  '\n{}{}[-]{} {}\n===={}\n'.format(colors.RED,colors.BOLD,colors.ENDC,string,len(string)*'=')
        elif sucess:return '\n{}{}[+]{} {}\n===={}\n'.format(colors.GREEN,colors.BOLD,colors.ENDC,string,len(string)*'=')
        elif info: return  '\n{}{}[*]{} {}\n===={}\n'.format(colors.BLUE,colors.BOLD,colors.ENDC,string,len(string)*'=')
    else:
        if   error:return  '{}{}[-]{} {}'.format(colors.RED,colors.BOLD,colors.ENDC,string)
        elif sucess:return '{}{}[+]{} {}'.format(colors.GREEN,colors.BOLD,colors.ENDC,string)
        elif info: return  '{}{}[*]{} {}'.format(colors.BLUE,colors.BOLD,colors.ENDC,string)

def banner():
    ASCII = ("""
                 ))))
                 ||||
                 |  @___oo  ---------------------------------
       /\  /\   / (__,,,,| | BOTNET SSH Manager              |
      ) /^\) ^\/ B)        | :::BOTdr4g0n::: / \/ \          |
      )   /^\/   O)        |                (/ //_ \_        |
      )   _ /  / T)        |                \||  .  \        |
  /\  )/\/ ||  | )_)       |           _,:__.-"/---\_ \      |
 <  >      |(,,) )N_)      |           '~-'--.)__( , )\ \    |
  ||      /    \)_E_)\     |Author: Marcos Nesster (mh4x0f)  |
  | \____(      )_T_) )___ |Version:/x1.1/ copyright 2014 `  |
   \______(_______;;; __;;;|---------------------------------|\n""")
    return ASCII