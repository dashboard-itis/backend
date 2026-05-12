import os

bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')
worker_class = 'uvicorn.workers.UvicornWorker'
workers = int(os.getenv('WEB_CONCURRENCY', '2'))
timeout = int(os.getenv('GUNICORN_TIMEOUT', '60'))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', '5'))
accesslog = '-'
errorlog = '-'
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
control_socket_disable = True
