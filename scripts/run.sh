#!/bin/bash
# Activate virtual environment
. /appenv/bin/activate

pip3.5 install -r requirements.txt

exec $@