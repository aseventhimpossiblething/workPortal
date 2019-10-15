


"""
print(os.environ['REDIS_URL'])

app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']


celery = Celery(app.name, broker=os.environ['REDIS_URL'])
celery.conf.update(app.config)
"""

