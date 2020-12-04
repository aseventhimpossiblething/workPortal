#!/bin/bash
sleep 5
gunicorn -c appconfig.py bdx-api-link:app
