NUM_WOKERS=6
timeout=120
#accesslog="/var/log/gunicorn/access.log"
#errorlog="/var/log/gunicorn/error.log"
accesslog="/var/www/workPortal/Sheets/access.log"
errorlog="/var/www/workPortal//Sheetserror.log"




#--access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log
bind="127.0.0.1:5000"
