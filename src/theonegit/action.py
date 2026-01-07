import os, pathlib
from . import complete, git, cmd

actions= {}
def register( actionName, actionFunction ):
    global actions
    actions[actionName]= actionFunction

def doHelp( arguments ):
	print( f"-- help --" )
	print( ", ".join( [str(a) for a in actions ] ) ) 

register( "help", doHelp )
register( "complete", complete.doComplete )

def doList( arguments ):
    target= []
    if len( arguments ) > 1 :
        target= arguments[1:]
    gits= git.makeList(target)
    print( git.stringList(gits) )

actions["list"]= doList

def doDo( arguments ):
    RED= '\033[0;31m'
    LIGHT= '\033[1;34m'
    NC= '\033[0m' # No Color

    rootPath= pathlib.Path().absolute()
    gits= git.makeList()
    command= ' '.join(arguments[1:])

    for depot in gits :
        os.chdir( depot.path )
        print( RED + '> ' + LIGHT + depot.path + NC)
        cmd.execute( command, verbose=False )
        os.chdir( rootPath )

actions["do"]= doDo

def doStatus(arguments):
    RED= '\033[0;31m'
    LIGHT= '\033[1;34m'
    NC= '\033[0m' # No Color

    rootPath= pathlib.Path().absolute()
    gits= git.makeList()
    command= 'git status -sb'

    for depot in gits :
        os.chdir( depot.path )
        print( RED + '> ' + LIGHT + depot.path + NC)
        cmd.execute( command, verbose=False )
        os.chdir( rootPath )

actions["status"]= doStatus
