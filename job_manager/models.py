from django.db import models


# Create your models here.


class JobTask(models.Model):
    """
    任务队列
    """
    STATUS = (
        ('waiting', '等待中'),
        ('running', '执行中'),
        ('finished', '完成'),
        ('interrupt', '中断'),
    )
    name = models.CharField('任务名', max_length=256)
    start_time = models.IntegerField('开始时间', null=True, blank=True)
    end_time = models.IntegerField('结束时间', null=True, blank=True)
    username = models.CharField('执行者', max_length=100)
    status = models.CharField('状态', max_length=100, choices=STATUS)
    params = models.TextField('参数', null=True, blank=True)
    error = models.TextField('错误信息', null=True, blank=True)
    confirm = models.BooleanField('结果确认', default=False)
    serial = models.CharField('串行标识', max_length=20, default='')
    package_src = models.CharField('包路径', max_length=100, null=True, blank=True)
    function_name = models.CharField('函数名', max_length=100)

    class Meta:
        ordering = ('-start_time',)

    def __str__(self):
        return self.name


class JobCmd(models.Model):
    """
    任务命令
    """
    RUN_TYPE = (
        ('local', '本地'),
        ('salt_sync', 'salt同步'),
        ('salt_async', 'salt异步'),
    )
    STATUS = (
        ('waiting', '等待中'),
        ('running', '执行中'),
        ('success', '完成'),
        ('failed', '失败'),
    )
    cmd = models.TextField(verbose_name='命令')
    run_type = models.CharField(verbose_name='运行类型', choices=RUN_TYPE, max_length=20)
    start_time = models.IntegerField(verbose_name='开始时间', null=True, blank=True)
    end_time = models.IntegerField(verbose_name='结束时间', null=True, blank=True)
    jid = models.IntegerField('jid', null=True, blank=True)
    status = models.CharField('状态', choices=STATUS, max_length=20)
    error = models.TextField('错误信息', null=True, blank=True)
    out = models.TextField('输出信息', null=True, blank=True)
    job_task = models.ForeignKey('job_manager.JobTask', verbose_name='任务', related_name='cmds', on_delete=models.CASCADE)

    def __str__(self):
        return self.cmd
