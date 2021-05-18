#!/bin/bash
sleep 5
cd /GMDelight/workPortal
#gunicorn -c appconfig.py bdx-api-link:app
gunicorn --bind=127.0.0.1:8000 bdx-api-link:app
