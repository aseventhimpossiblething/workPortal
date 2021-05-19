#!/bin/bash
sleep 2
cd /GMDelight/GMDelight/
gunicorn -c appconfig.py bdx-api-link:app
