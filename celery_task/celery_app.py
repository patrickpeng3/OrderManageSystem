import os
from celery import Celery, platforms
from django.conf import settings


# 允许root用户运行celery
platforms.C_FORCE_ROOT = True

# 为celery设置环境变量
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb_hls.settings')

# 创建应用
app = Celery("celery_cmdb")

# 配置应用
app.config_from_object('celery_task.celeryconfig')

# 自动搜索任务
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()

