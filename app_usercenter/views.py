from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from app_usercenter import models
from wechatpy.oauth import WeChatOAuth
from common.config import CONF
from common.log import MAIN_LOG
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatJSAPI
from wechatpy.session import SessionStorage
from wechatpy.replies import TextReply
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException

import time
import json
import hashlib
import datetime
import random
import traceback

WX_CLIENT = WeChatClient(
    CONF['app_id'],
    CONF['app_secret']
)

WEJS = WeChatJSAPI(client=WX_CLIENT)
RANDOM_STR_RANGE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"



def get_js_api_info(request):
    url = request.GET.get('url')
    ret = dict()
    ret['app_id'] = CONF['app_id']
    ret['noncestr'] = ''.join(random.choice(RANDOM_STR_RANGE) for _ in range(8))
    ret['timestamp'] = int(time.time())
    ret['url'] = url

    ticket = WEJS.get_jsapi_ticket()
    ret['signature'] = WEJS.get_jsapi_signature(ret['noncestr'], ticket, ret['timestamp'], ret['url'])
    print('get_js_api_info!!!', ret)

    return HttpResponse(json.dumps({'status': 'ok', 'data': ret}))


def index(request):
    return HttpResponse('hello usercenter! %s' % request.__dict__['website_cookie'])


def login(request):
    if request.__dict__['method'] == 'GET':
        return render(request, 'jqweui/login.html')

    if request.__dict__['method'] == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        last_url = request.GET.get('last_url', '')

        print(user, pwd)
        user_ret = models.User.objects.filter(user_name=user, user_passwd=pwd)
        if len(user_ret) == 0:
            return render(request, 'jqweui/login.html', {'msg': '账号或密码错误!'})
        request.__dict__['set_cookie'] = True
        request.__dict__['set_cookie_user'] = user_ret[0].wx_openid
        if last_url == '':
            return redirect('/%s/website/index.html' % CONF['site_name'])
        else:
            return redirect(last_url)


def wx_login(request):
    last_url = request.GET.get('last_url', None)
    if last_url is None or last_url == '':
        redirect_uri = 'http://%s/%s/usercenter/login.html' % (CONF['site_domain'], CONF['site_name'])
    else:
        redirect_uri = 'http://%s/%s/usercenter/login.html?last_url=%s' % (CONF['site_domain'], CONF['site_name'], last_url)
    print('redirect_uri!!!!!', redirect_uri)
    code = request.GET.get('code', None)
    scope = 'snsapi_userinfo'
    _state = None
    wechat_oauth = WeChatOAuth(CONF.get('app_id'), CONF.get('app_secret'), redirect_uri, scope, _state)
    if code is None:
        # authorize_url 跳转授权
        # qrconnect_url 扫码授权
        return redirect(getattr(wechat_oauth, 'authorize_url'))

    res = wechat_oauth.fetch_access_token(code)
    '''
    res:
    {
      'access_token': '22_fzZEb4_hNIfZlpYFA3z4gbFd41ZRbACtXjA835hpbOqezgV6z6Oe306O-nd9kEgntAKE33kxAgPM_Kula4JWCxwm5kgvqhsCPIjT32NRxOk',
      'expires_in': 7200,
      'refresh_token': '22_7u50NJLDqVNYIAZ_FbS9Uh71zmD-ur_1P3n2CJGCoN2pNcbZfl8THRxMrxUrTRbWgw9nmU9jgcdZPA9k29zdxk94GfdkP6saPA96sXhkc4I',
      'openid': 'obQM66ENepzE1XAT49pohxVmW9zM',
      'scope': 'snsapi_userinfo'
    }
    '''

    user_info = wechat_oauth.get_user_info()
    '''
    user_info:
    {
      'openid': 'obQM66ENepzE1XAT49pohxVmW9zM',
      'nickname': '胡同口儿王大爷',
      'sex': 1,
      'language': 'zh_CN',
      'city': '海淀',
      'province': '北京',
      'country': '中国',
      'headimgurl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epRHYTGEDnmSZ9ASdTW0HUGCc7Hr9sMSuldicxl0mhbh6C7IBe8oQuHcibpstwYpncatibib1icvbibrkfA/132',
      'privilege': [
      ]
    }
    '''

    describe_info = WX_CLIENT.user.get(user_info['openid'])
    '''
    describe_info
    {
      'subscribe': 1,
      'openid': 'obQM66ENepzE1XAT49pohxVmW9zM',
      'nickname': '胡同口儿王大爷',
      'sex': 1,
      'language': 'zh_CN',
      'city': '海淀',
      'province': '北京',
      'country': '中国',
      'headimgurl': 'http://thirdwx.qlogo.cn/mmopen/ajNVdqHZLLCsSogzyNjMmibOOMC4AkkAdgkjPgEJ6s8iaek2MI04ibcia2H5lNoEF1Dv7VgetkyB2BtnFemvY4jvicA/132',
      'subscribe_time': 1551935444,
      'remark': '',
      'groupid': 0,
      'tagid_list': [
      ],
      'subscribe_scene': 'ADD_SCENE_PROFILE_CARD',
      'qr_scene': 0,
      'qr_scene_str': ''
    }
    '''
    try:
        ret = models.User.objects.filter(wx_openid=user_info['openid'])
        MAIN_LOG.logger.debug("user login ret: %s" % user_info['nickname'])
    except Exception as e:
        return redirect("/%s/usercenter/notrss.html" % CONF['site_name'])

    if describe_info['subscribe'] == 0:
        # 如果没有关注公众号
        describe_info['province'] = user_info['province']
        describe_info['city'] = user_info['city']
        describe_info['subscribe_time'] = int(time.time())
        describe_info['headimgurl'] = user_info['headimgurl']
        describe_info['language'] = user_info['language']
        describe_info['openid'] = user_info['openid']
        describe_info['country'] = user_info['country']
        describe_info['nickname'] = user_info['nickname']
        describe_info['sex'] = user_info['sex']

    if len(ret) == 0:
        _tmp = {
            'wx_province': describe_info['province'],
            'wx_city': describe_info['city'],
            'wx_subscribe_time': datetime.datetime.fromtimestamp(describe_info['subscribe_time']),
            'wx_headimgurl': describe_info['headimgurl'],
            'wx_language': describe_info['language'],
            'wx_openid': describe_info['openid'],
            'wx_country': describe_info['country'],
            'wx_nickname': describe_info['nickname'],
            'wx_sex': describe_info['sex'],
            'wx_subscribe': describe_info['subscribe'],
            'wx_json': json.dumps(describe_info),
        }
        models.User.objects.create(**_tmp)
        ret = models.User.objects.filter(wx_openid=describe_info['openid'])

    request.__dict__['set_cookie'] = True
    request.__dict__['set_cookie_user'] = ret[0].wx_openid
    funvar = {"user_name": ret[0].wx_openid, "login_time": int(time.time()),
              "cookies": request.COOKIES.get('s'), "user_table_id": -1, "last_action": int(time.time())}

    request.__dict__["website_cookie"] = funvar

    if last_url is None or last_url == '':
        return redirect('/%s/usercenter/index.html' % CONF['site_name'])
    else:
        return redirect(last_url)


def upload(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status': 'error', 'msg': 'method is not post'}))
    try:
        wx_openid = request.__dict__['website_cookie']['user_name']
        user_obj = models.User.objects.get(wx_openid=wx_openid)
        file_obj = request.FILES.get('file_obj')
        user_obj.user_image = file_obj
        user_obj.save()
        return HttpResponse(json.dumps({'status': 'ok', 'msg': '上传成功'}))

    except Exception as e:
        return HttpResponse(json.dumps({'status': 'error', 'msg': e}))