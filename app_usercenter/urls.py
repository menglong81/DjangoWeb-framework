#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:urls.py

from django.conf.urls import url
from app_usercenter import views


urlpatterns = [
    url(r'^login.html', views.wx_login),
    url(r'^dev_login.html', views.login),
    url(r'^index.html', views.index),
    url(r'^get_js_api_info', views.get_js_api_info),
    url(r'^upload.html', views.upload)
]