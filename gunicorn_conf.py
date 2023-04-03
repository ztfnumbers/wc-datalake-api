from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/home/sndjeng/api/api_ztfnumbers/api/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/sndjeng/api/api_ztfnumbers/api/logs/access_log'
errorlog =  '/home/sndjeng/api/api_ztfnumbers/api/logs/error_log'