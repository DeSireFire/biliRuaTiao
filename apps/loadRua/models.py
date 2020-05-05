from django.db import models

# Create your models here.
class biliUser(models.Model):
    buser = models.CharField(max_length=255, verbose_name='账号', unique=True)
    bpw = models.CharField(max_length=255, verbose_name='密码', unique=True)

    # 解决objects报警告
    objects = models.Manager()

    def __str__(self):
        return self.buser

    class Meta:
        verbose_name = 'B站账号信息'
        db_table = "biliUser"
        verbose_name_plural = verbose_name