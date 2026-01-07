import os, re
from . import cmd

class Git :
	def __init__(self, path) :
		self.path= path
		self.remotes= {}

	def addRemote(self, name, url):
		self.remotes[name]= url

	def directory(self) :
		return self.path

	def __str__(self):
		s= self.path
		for name in self.remotes :
			s+= f'\n- {name}: {self.remotes[name]}'
		return s


def loadList( fileName ):
	patern = re.compile('- ([\S]*): ([\S]*)')
	git= None
	gits= []
	fileDsc= open( fileName, 'r' )

	for line in fileDsc :
		repo= patern.match(line)
		if patern.match(line) :
			git.addRemote( repo[1], repo[2] )
		else :
			git= Git( line[:-1] )
			gits.append( git )

	return gits

def makeList( decendents= [] ):
	gits= []
	dirs= []
	forbidden= [ "", ".", "..", "Archives", "Games", "Téléchargements", "Trash", "Fun", "Large", "snap", "Shared", "Zomboid" ]

	def validChildren( son, son_path ):
		return son not in forbidden and os.path.isdir( son_path ) and son[0] != '.'

	if len( decendents ) == 0 :
		decendents= cmd.query( 'ls .' )
	
	for son in decendents :
		son_path = './'+ son
		if validChildren(son, son_path) :
			dirs.append( son_path )

	while len(dirs) > 0 :
		elt = dirs.pop(0) # for each directory
		decendents= cmd.query( 'ls -a "'+ elt + '"' )
		#print( "> visit: "+ elt )

		# test if it is a git repo
		if ".git" in decendents and os.path.isdir( elt+"/.git" ) :
			git= Git( elt[2:] )
			remotes= cmd.query( 'git -C "'+ elt + '" remote' )
			for name in remotes :
				url= cmd.query( 'git -C "'+ elt + '" remote get-url '+ name )[0]
				git.addRemote(name, url)
				#print('#  - '+name+': '+ url  )
			gits.append( git )
			decendents= cmd.query( 'ls -a "'+ elt + '"' )

		else :
			# Add decendents directories to process list
			subdirs= []
			for son in decendents :
				son_path = elt +'/'+ son
				if validChildren(son, son_path) :
					subdirs.append( son_path )
			dirs = subdirs + dirs

	return gits

def directories( gits ):
	dirs= [ g.path for g in gits ]
	return dirs

def stringList( aList ):
	return '\n'.join( [ str(elt) for elt in aList ] )