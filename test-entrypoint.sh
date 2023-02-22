#!/bin/bash
#This is an autogenerated file
VENV_NAME=".venv"
# activate virtual environment
source "$VENV_NAME/bin/activate"
# run the python program
# the output from a command is required
python test-entrypoint.py "$@"
# deactivate virtual environment
deactivate