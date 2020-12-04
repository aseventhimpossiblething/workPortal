#!bin/bash
cd gunicorn -c appconfig.py bdx-api-link:app --daemon
