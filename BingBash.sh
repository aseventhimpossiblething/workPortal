#!/usr/bin/env bash
pwd
cd /var/www/workPortal
pwd
gunicorn -c var/www/workPortal/appconfig.py bdx-api-link:app
tail -F /var/www/workPortal/Sheets/error.log
