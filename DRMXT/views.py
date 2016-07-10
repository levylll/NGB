#coding:utf-8
from django import template
from django import forms
from django.http import HttpResponse,Http404
from django.shortcuts import render,render_to_response
from django.template import Context,loader
from django.views.generic import View,TemplateView,ListView,DetailView
from django.db.models import Q
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from DRMXT.models import LogCls
from vmaig_comments.models import Comment
from vmaig_auth.models import VmaigUser
from vmaig_auth.forms import VmaigUserCreationForm,VmaigPasswordRestForm
from vmaig_blog.settings import PAGE_NUM
import datetime,time
import json
import logging
from django_extlog.models import ExtLog

#缓存
try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']

#logger
logger = logging.getLogger(__name__)


class BaseMixin(object):

    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin,self).get_context_data(**kwargs)
        return context

class DRMXTView(BaseMixin,ListView):
    template_name = 'blog/drmxt.html'
    context_object_name = 'comment_list'
    def get_context_data(self,**kwargs):
        #轮播
        buf = LogCls.objects.all()
        kwargs['comment_list'] = buf[:5]
        return super(DRMXTView,self).get_context_data(**kwargs)

    def get_queryset(self):
        comment_list = ExtLog.objects.all()[:5]
        return comment_list

        mydict = {"errors":""}
        return HttpResponse(json.dumps(mydict),content_type="application/json")
