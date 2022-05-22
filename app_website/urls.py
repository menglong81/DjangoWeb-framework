#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:urls.py

from django.conf.urls import url
from app_website import views

urlpatterns = [

    url(r'index.html', views.index),

    url(r'quick_record.html', views.quick_record)

]
