#!/bin/bash
sleep 2
cd /GMDelight/workPortal/
gunicorn -c appconfig.py bdx-api-link:app
