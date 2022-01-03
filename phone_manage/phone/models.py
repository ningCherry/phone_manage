from django.db import models

# Create your models here.

class LoginUser(models.Model):
    username=models.CharField(max_length=10,verbose_name='用户名',blank=False,unique=True)
    password=models.CharField(max_length=10,verbose_name='密码',blank=False)


class DeviceInfo(models.Model):
    center_name=models.CharField(max_length=10,verbose_name='所属中心',blank=False,default='一中心')  #blank设置为True时，字段可以为空。设置为False时，字段是必须填写的
    device_name=models.CharField(max_length=20,verbose_name='资产名称',blank=False)
    device_system=models.CharField(max_length=10,verbose_name='设备系统',blank=False)
    device_factory=models.CharField(max_length=10,verbose_name='厂商',blank=False)
    device_system_version=models.CharField(max_length=20,verbose_name='系统版本',blank=False)
    device_asset_num=models.CharField(max_length=20,verbose_name='资产编号',unique=True,blank=False)
    device_phone_num=models.CharField(max_length=20,verbose_name='手机号码',blank=False)
    device_recipient=models.CharField(max_length=20,verbose_name='出库领用人')
    device_user=models.CharField(max_length=20,verbose_name='使用人')
    creator = models.CharField(max_length=20, verbose_name="创建人")
    create_date=models.DateTimeField(verbose_name='创建日期')
    update_data=models.DateTimeField(verbose_name='更新日期')
    device_img=models.ImageField(upload_to='device_img',default="")
    asser_img=models.ImageField(upload_to='asser_img',default="")

class CirculationInfo(models.Model):
    device_asset_num = models.ForeignKey(DeviceInfo,verbose_name='资产编号',on_delete=models.CASCADE)
    device_user = models.CharField(max_length=20, verbose_name='使用人')
    creator = models.CharField(null=True, max_length=20, verbose_name="创建人")
    handover_reason = models.CharField(null=True, max_length=20, verbose_name="交接原因")
    created_date = models.DateTimeField(verbose_name="创建日期")
    update_data = models.DateTimeField(verbose_name="更新日期")




