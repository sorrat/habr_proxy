from config import settings


bind = '{0.HOST}:{0.PORT}'.format(settings)
workers = 2
threads = 2
keepalive = 4
loglevel = 'debug'
errorlog = '-'
accesslog = '-'
reload = True
