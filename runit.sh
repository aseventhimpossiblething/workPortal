#!/bin/bash
sleep 10
gunicorn -c appconfig.py bdx-api-link:app --daemon
