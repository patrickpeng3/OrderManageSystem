from multiprocessing import cpu_count
from kombu import Exchange, Queue
import os
import sys
sys.path.append('/data/gitlab/oam-admin/cmdb_hls')

# 设置celery时区
CELERY_TIMEZONE = "Asia/Shanghai"

# 中间人
BROKER_URL = "amqp://root:root@localhost:5672/celery_host"

# 存储结果
# CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

# 缓存后端
CELERY_CACHE_BACKEND = 'django-cache'
