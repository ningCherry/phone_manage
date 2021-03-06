# Generated by Django 3.2.6 on 2021-08-15 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('center_name', models.CharField(default='一中心', max_length=10, verbose_name='所属中心')),
                ('device_name', models.CharField(max_length=20, verbose_name='资产名称')),
                ('device_system', models.CharField(max_length=10, verbose_name='设备系统')),
                ('device_factory', models.CharField(max_length=10, verbose_name='厂商')),
                ('device_system_version', models.CharField(max_length=20, verbose_name='系统版本')),
                ('device_asset_num', models.CharField(max_length=20, unique=True, verbose_name='资产编号')),
                ('device_phone_num', models.IntegerField(verbose_name='手机号码')),
                ('device_recipient', models.CharField(max_length=20, verbose_name='出库领用人')),
                ('device_user', models.CharField(max_length=20, verbose_name='使用人')),
                ('creator', models.CharField(max_length=20, verbose_name='创建人')),
                ('create_date', models.DateTimeField(verbose_name='创建日期')),
                ('update_data', models.DateTimeField(verbose_name='更新日期')),
                ('device_img', models.ImageField(default='', upload_to='device_img')),
                ('asser_img', models.ImageField(default='', upload_to='asser_img')),
            ],
        ),
        migrations.CreateModel(
            name='LoginUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=10, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='CirculationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_user', models.CharField(max_length=20, verbose_name='使用人')),
                ('creator', models.CharField(max_length=20, null=True, verbose_name='创建人')),
                ('handover_reason', models.CharField(max_length=20, null=True, verbose_name='交接原因')),
                ('created_date', models.DateTimeField(verbose_name='创建日期')),
                ('update_data', models.DateTimeField(verbose_name='更新日期')),
                ('device_asset_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phone.deviceinfo', verbose_name='资产编号')),
            ],
        ),
    ]
