#!/bin/bash
sleep 2
cd /GMDelight/workPortal/
gunicorn --bind=127.0.0.1:8000 bdx-api-link:app
