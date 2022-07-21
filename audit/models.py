from django.db import models
from users.models import User
import uuid

# Create your models here.


class ssh_audit(models.Model):
    uuid = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(u"操作用户", max_length=20)
    bash_shell = models.TextField(u"命令")
    audit_data_time = models.DateTimeField(u"操作时间")
    server_ip = models.GenericIPAddressField("u服务器ip")

    def __unicode__(self):
        return self.user_name

    class Meta:
        verbose_name = u"审计"
        verbose_name_plural = verbose_name
