#!bin/bash
gunicorn -c appconfig.py bdx-api-link:app --daemon
