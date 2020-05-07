NUM_WOKERS=6
TIMEOUT=120
accesslog="/var/log/gunicorn/access.log"
errorlog="/var/log/gunicorn/error.log"



#--access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log
bind="127.0.0.1:5000"
