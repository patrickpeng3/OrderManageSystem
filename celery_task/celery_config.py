from multiprocessing import cpu_count
from kombu import Exchange, Queue
import os
import sys
sys.path.append('/data/gitlab/oam-admin/cmdb_hls')

# 设置celery时区
timezone = "Asia/Shanghai"

# 中间人
broker_url = "amqp://root:root@localhost:5672/celery_host"

# 存储结果
result_backend = "django-db"

# 缓存后端
cache_backend = 'django-cache'
