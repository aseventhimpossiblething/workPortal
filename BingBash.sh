#!/usr/bin/env bash
pwd
cd /var/www/workPortal
pwd
gunicorn -c appconfig.py bdx-api-link:app
tail -F Sheets/error.log
