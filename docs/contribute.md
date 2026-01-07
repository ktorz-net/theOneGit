# Contribute to theOneGit


## Create a new sub-command.

A `tog` subcommand like do or list is an action in `tog` environment.

## Set-up a new action.

So, first create a source file for your new action. 
For instance, create the file `actionExemple.py` into the `src/theonegit` directory.
The `actionExemple.py` include at least $2$ element: the function to process and a registration with a action name.

```python
from . import action

def doExemple( arguments ):
	print( f"-- Exemple {arguments}--" )

action.register( "exemple", doExemple )
```

Last action from developer side consists in importing the `actionExemple` sub-package in the `__main__.py` file, line $1$.

Then install again theOneGit, the `exemple` subcommand should be functional.

```sh
pip install .
tog help
tog exemple
```
