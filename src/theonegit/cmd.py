"""
Created on Feb 13 2019

@author: G. Lozenguez
"""

import os, sys, re

# Environment :
rootDir= os.environ['HOME']
#shareDir= rootDir + "/share"
tmpDir= rootDir+"/.tog/tmp"

# Parameters :
class Parameter :
    def __init__(self, name, letter= '', numberOfArgument= 0, description= ''):
        self.name= name
        self.letter= letter
        self.expectedArgs= numberOfArgument
        self.value= False
        self.descrittion= description

def parseParameters( parameters, arguments, expectedArguments= None ):
	return True, {}, arguments[1:]

# Commande generation :
def execute(cmd, verbose= True):
  if verbose :
      print(cmd)
  os.system( cmd )

def query(cmd, verbose= False):
    tpath= tmpDir +"/" + str(os.getpid()) +".txt"
    ccmd= cmd +" > "+ tpath +" 2>&1"
    # print if asked:
    if verbose :
        print( ccmd )
    # execute:
    os.system( ccmd )
    # return the result:
    fdsc=  open( tpath, 'r')
    content= []
    for line in fdsc :
        content.append(line.rstrip())
    fdsc.close()
    return content

# git commande :
def git(cmd, location, verbose= False):
    return query( 'git -C '+ location +" "+ cmd, verbose)

def gitStatus(elt, location, verbose= False):
    #Exemple of elt: Fichiers non suivis, rien a valider, ...
    status= git(
        'status | grep "'+ elt +'"',
        location, verbose )
    return len( status ) > 0

# report :
def open_report(fileName= "report.log"):
    path+= tmpDir+ fileName
    execute("rm "+ path + " 2> /dev/null", False)
    execute("touch "+ path, False)
    return open( path, 'w' )

def buildList( listInput ):

	pathRe= re.compile(".+")
	repoRe= re.compile("  - (.+): (.+)")

	dico= {}
	current= ''

	for line in listInput:
		repo= repoRe.match(line)
		if repo :
			dico[ current ].append( [repo.group(1), repo.group(2)] )
		else :
			current = pathRe.match(line).group(0)
			dico[ current ] = []

	return dico
