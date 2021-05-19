NUM_WOKERS=20
timeout=300
#accesslog="/var/log/gunicorn/access.log"
#errorlog="/var/log/gunicorn/error.log"
accesslog="/var/www/workPortal/Sheets/access.log"
errorlog="/var/www/workPortal/Sheets/error.log"




#--access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log
bind="127.0.0.1:8000"
