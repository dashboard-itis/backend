import multiprocessing
import os

bind = '0.0.0.0:8000'
worker_class = 'uvicorn.workers.UvicornWorker'
workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
timeout = int(os.getenv('GUNICORN_TIMEOUT', '60'))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', '5'))
accesslog = '-'
errorlog = '-'
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
