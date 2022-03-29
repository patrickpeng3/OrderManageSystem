from django.db import models

# Create your models here.


# 会员模型
class member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=5)
    number = models.DecimalField(max_digits=11, decimal_places=0)
    address = models.CharField(max_length=50)
    status = models.IntegerField

    class Meta:
        verbose_name = "会员"

