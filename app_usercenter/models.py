from django.db import models

# Create your models here.

'''
微信传送的用户格式
{
  "province": "北京",
  "city": "海淀",
  "subscribe_time": 1558021879,
  "headimgurl": "http://thirdwx.qlogo.cn/mmopen/ajNVdqHZLLDt7t1qdEgBuDTtJzIcPbWPyCG4gsdGibtibcSiby2OQs2HgSPpuTbDI5VVn4D5wzcgzFJEO6bM1rYYA/132",
  "language": "zh_CN",
  "openid": "o-brwvtbzoLI8q51Wj7znAYMNzss",
  "country": "中国",
  "tagid_list": [
  ],
  "remark": "",
  "qr_scene": 0,
  "sex": 1,
  "qr_scene_str": "",
  "subscribe": 1,
  "user_name": "胡同口儿王大爷",
  "nickname": "胡同口儿王大爷",
  "groupid": 0,
  "subscribe_scene": "ADD_SCENE_PROFILE_CARD"
}
'''


class User(models.Model):
    class Meta:
        verbose_name_plural = '用户信息'
        verbose_name = '用户信息'

    user_name = models.CharField(max_length=32, null=True, blank=True, verbose_name='用户名',
                                 help_text='只有登录模式为local时才会启用账号密码登陆')
    user_passwd = models.CharField(max_length=32, null=True, blank=True, verbose_name='用户密码',
                                   help_text='只有登录模式为local时才会启用账号密码登陆')

    user_image = models.ImageField(upload_to='user_header/', null=True, blank=True, verbose_name='用户头像')

    wx_province = models.CharField(max_length=32, null=True, blank=True, verbose_name='微信_省')
    wx_city = models.CharField(max_length=32, null=True, blank=True, verbose_name='微信_市')
    wx_subscribe_time = models.DateTimeField(null=True, blank=True, verbose_name='微信_订阅时间')
    wx_headimgurl = models.CharField(max_length=256, null=True, blank=True, verbose_name='微信_头像')
    wx_language = models.CharField(max_length=32, null=True, blank=True, verbose_name='微信_用户语言')
    wx_openid = models.CharField(max_length=128, null=False, blank=False, unique=True, verbose_name='微信_openid')
    wx_country = models.CharField(max_length=32, null=True, blank=True, verbose_name='微信_国家')
    wx_nickname = models.CharField(max_length=32, null=True, blank=True, verbose_name='微信_昵称')
    wx_sex_dict = (
        (0, '女'),
        (1, '男'),
    )
    wx_sex = models.IntegerField(choices=wx_sex_dict, null=True, blank=True, verbose_name='微信_性别')
    wx_subscribe_dict = (
        (0, '否'),
        (1, '是'),
    )
    wx_subscribe = models.IntegerField(choices=wx_subscribe_dict, null=True, blank=True, verbose_name='微信_是否订阅')
    wx_json = models.TextField(max_length=1024, null=True, blank=True, verbose_name='微信_json全部')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    def __str__(self):
        return self.wx_nickname