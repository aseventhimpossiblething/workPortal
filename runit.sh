#!/bin/bash
sleep 2
echo "$PWD"
cd /GMDelight/workPortal/
echo "$PWD"
gunicorn --bind=127.0.0.1:8000 bdx-api-link:app --daemon
