#!/usr/bin/env bash

# Go at the root directory of the project 
cd `dirname $0`/..

# and update
git pull
pip install .
