from celery_task.celery_app import app


@app.task(bind=True)
def my_task():
    print("输出：test")
    return "返回:test"
