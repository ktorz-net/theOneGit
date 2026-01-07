from . import action
from . import complete, git, cmd

def doClone( arguments ):
	print( f"-- clone {arguments}" )
	repoList= git.loadList( arguments[1] )
	for repo in repoList :
		cmd.execute( 'git clone ' + repo.remotes['origin'] +' '+ repo.path)
		for name in repo.remotes :
			if name != 'origin' :
				cmd.execute( 'git -C '+ repo.path +' remote add ' + name  +' '+ repo.remotes[name] )

action.register( "clone", doClone )
