#!/usr/bin/env bash
cd /var/www/workPortal
gunicorn -c var/www/workPortal/appconfig.py bdx-api-link:app
tail -F /var/www/workPortal/Sheets/error.log
