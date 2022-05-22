from django.contrib import admin
from app_usercenter import models as user_models

admin.site.site_header = "{#APPNAME#}"
admin.site.site_title = "{#APPNAME#}"

# Register your models here.
@admin.register(user_models.User)
class User(admin.ModelAdmin):
    list_display = ('id', 'wx_openid', 'wx_nickname', 'wx_sex', 'wx_province', 'wx_city', 'create_time')
    search_fields = ('wx_nickname', 'wx_openid')
    toexcel_fields = ('id', 'wx_openid', 'wx_nickname', 'wx_sex', 'wx_province', 'wx_city', 'create_time')
    toexcel_tags = ('id', '微信openid', '微信昵称', '性别', '省份', '城市', '数据创建时间')
    toexcel_choices_fields = ('user_type',)
    toexcel_choices_dict = ('user_type_dict',)