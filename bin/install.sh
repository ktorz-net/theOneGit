#!/usr/bin/env bash
ONEPATH="$( cd -- "$(dirname "$0"/..)" >/dev/null 2>&1 ; pwd -P )"

# Go at the root directory of the project 
cd `dirname $0`/..

# Install...
pip install .

# setup shell environment
echo """
# TheOneGit
export THE_ONE_GIT=$ONEPATH
source \$THE_ONE_GIT/bin/run-commands.bash
""" >> ~/.bashrc

echo """
# TheOneGit
export THE_ONE_GIT=$ONEPATH
source \$THE_ONE_GIT/bin/run-commands.zsh
""" >> ~/.zshrc
