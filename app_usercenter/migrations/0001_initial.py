# Generated by Django 2.2.2 on 2021-03-05 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, help_text='只有登录模式为local时才会启用账号密码登陆', max_length=32, null=True, verbose_name='用户名')),
                ('user_passwd', models.CharField(blank=True, help_text='只有登录模式为local时才会启用账号密码登陆', max_length=32, null=True, verbose_name='用户密码')),
                ('user_image', models.ImageField(blank=True, null=True, upload_to='user_header/', verbose_name='用户头像')),
                ('wx_province', models.CharField(blank=True, max_length=32, null=True, verbose_name='微信_省')),
                ('wx_city', models.CharField(blank=True, max_length=32, null=True, verbose_name='微信_市')),
                ('wx_subscribe_time', models.DateTimeField(blank=True, null=True, verbose_name='微信_订阅时间')),
                ('wx_headimgurl', models.CharField(blank=True, max_length=256, null=True, verbose_name='微信_头像')),
                ('wx_language', models.CharField(blank=True, max_length=32, null=True, verbose_name='微信_用户语言')),
                ('wx_openid', models.CharField(max_length=128, unique=True, verbose_name='微信_openid')),
                ('wx_country', models.CharField(blank=True, max_length=32, null=True, verbose_name='微信_国家')),
                ('wx_nickname', models.CharField(blank=True, max_length=32, null=True, verbose_name='微信_昵称')),
                ('wx_sex', models.IntegerField(blank=True, choices=[(0, '女'), (1, '男')], null=True, verbose_name='微信_性别')),
                ('wx_subscribe', models.IntegerField(blank=True, choices=[(0, '否'), (1, '是')], null=True, verbose_name='微信_是否订阅')),
                ('wx_json', models.TextField(blank=True, max_length=1024, null=True, verbose_name='微信_json全部')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
    ]
