from . import action

def doComplete( arguments ):
	print( "DoComplete: "+ str(arguments) )
	cmd= "tog"
	toComplete= "--"
	if len(arguments) >= 3:
		cmd= arguments[1]
		toComplete= arguments[2]
	if cmd == 'tog' :
		for a in action.actions :
			print( a )