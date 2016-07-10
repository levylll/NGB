#coding:utf-8
from django import template
from django import forms
from django.http import HttpResponse,Http404
from django.shortcuts import render,render_to_response,RequestContext
from django.template import Context,loader
from django.views.generic import View,TemplateView,ListView,DetailView
from django.db.models import Q
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from DSFYW.models import DsfywCls
from DRMXT.models import LogCls
from vmaig_comments.models import Comment
from vmaig_auth.models import VmaigUser
from vmaig_auth.forms import VmaigUserCreationForm,VmaigPasswordRestForm
from vmaig_blog.settings import PAGE_NUM
import datetime,time
from django_extlog.models import ExtLog
import json
import logging

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

class DSFYWView(BaseMixin,ListView):
    template_name = 'blog/dsfyw.html'
    context_object_name = 'comment_list'
    def get_context_data(self,**kwargs):
        #轮播
        kwargs['comment_list'] = DsfywCls.objects.all()[:3]
        return super(DSFYWView,self).get_context_data(**kwargs)

    def get_queryset(self):
        comment_list = DsfywCls.objects.all()
        return comment_list

    def post(self, request, *args, **kwargs):
        json_input = self.request.POST.get("json_input","")
        DsfywCls.objects.create(
                comment = json_input
                )
        indexed_ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print indexed_ts
        LogCls.objects.create(
                app_name = u'第三方业务',
                add_content = json_input,
                operator = 'add',
                create_time = indexed_ts
                )
        mydict = {"errors":""}
        return HttpResponse(json.dumps(mydict),content_type="application/json")
