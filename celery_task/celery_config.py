from multiprocessing import cpu_count
from kombu import Exchange, Queue
import os
import sys
sys.path.append('/data/gitlab/oam-admin/cmdb_hls')
from celery import Celery, platforms
platforms.C_FORCE_ROOT = True

# 设置celery时区
timezone = "Asia/Shanghai"

# 中间人
broker_url = "amqp://root:root@localhost:5672/celery_host"

# 存储结果
result_backend = "django-db"

# 缓存后端
cache_backend = 'django-cache'

# 将任务结果使用'pickle'序列化成'json'格式
# 任务序列化方式
task_serializer = 'pickle'

# 任务执行结果序列化方式
result_serializer = 'json'

# 指定任务接受的序列化类型.
accept_content = ['pickle', 'json']
