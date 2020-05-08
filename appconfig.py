NUM_WOKERS=6
timeout=120
accesslog="sudo /var/log/gunicorn/access.log"
errorlog="sudo /var/log/gunicorn/error.log"



#--access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log
bind="127.0.0.1:5000"
