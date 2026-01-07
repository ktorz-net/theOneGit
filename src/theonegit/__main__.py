from . import action, actionClone
import sys

def commandHandler():
    todo= "help"
    arguments= ["help"]
    
    if len(sys.argv) > 1 :
        todo= sys.argv[1]
        arguments= sys.argv[1:]
    
    if todo in action.actions.keys() :
        action.actions[todo]( arguments )
    else :
        action.actions["help"]( arguments )
    return 1

if __name__ == '__main__':
    commandHandler()
