#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Author:zino

from django.conf.urls import include, url
from django.contrib import admin
from blog.views import *

urlpatterns = [
    url(r'^blog/$',blog,name='blog'),
    url(r'^blog_video/$',blog_video,name='blog_video'),
    url(r'^blog_news/$',blog_news,name='blog_news'),
    url(r'^blog_picture/$',blog_picture,name='blog_picture'),
    url(r'^video/(?P<id>\d+)/$',video,name='video'),
    url(r'^article_details/(?P<id>\d+)/$',article_details,name='article_details'),
    url(r'^qiniu_video/$', qiniu_video, name='qiniu_video'),
    url(r'^uptoken/$', uptoken, name='uptoken'),
    url(r'^collection$', collection_time, name='collection'),
    url(r'^search$', blog_search, name='search'),
    url(r'^picture_details/(?P<id>[\d]+)/$', picture_details, name='picture_details'),
    url(r'^comment/(?P<id>[\d]+)/$', comment_post, name='comment_post'),

]