#!/bin/sh
cd controller
python3 movies.py

-T 'application/json' \
http://localhost:5000
