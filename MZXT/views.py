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
from MZXT.models import FieldCls
from DRMXT.models import LogCls
from RZSQ.models import SeqCls, RecordCls
from vmaig_comments.models import Comment
from vmaig_auth.models import VmaigUser
from vmaig_auth.forms import VmaigUserCreationForm,VmaigPasswordRestForm
from vmaig_blog.settings import PAGE_NUM
import datetime,time
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

class MzxtView(BaseMixin,ListView):
    template_name = 'blog/mzxt.html'
    context_object_name = 'comment_list'
    def get_context_data(self,**kwargs):
        fieldset = FieldCls.objects.all()
        tablenames = []
        for elem in fieldset:
            if elem.tablename not in tablenames:
                tablenames.append(elem.tablename)
        kwargs['tablelist'] = tablenames
        return super(MzxtView,self).get_context_data(**kwargs)

    def get_queryset(self):
        fieldset = FieldCls.objects.all()
        tablelist = []
        for elem in fieldset:
            if elem.tablename not in tablelist:
                tablelist.append(elem.tablename)
        return tablelist

    def post(self, request, *args, **kwargs):
        fname = self.request.POST.get('fname')
        if not fname:
            sendinfo = self.request.body
            sendinfo = json.loads(sendinfo)
            tablename = sendinfo['tablename']
            rowinfo = sendinfo['rows']
            time_now = datetime.datetime.now()
            count=0
            record = ''
            for row in rowinfo:
                count=count+1
                res = FieldCls.objects.create(  tablename = tablename,\
                                                field_name = row['name'],\
                                                field_type = row['type'],\
                                                create_time = time_now
                                              )
                record = record + row['name'] + ':' + row['type'] + ','
            LogCls.objects.create(
                app_name = u'媒资系统',
                add_content = record[:-1],
                operator =  '创建表【%s】，并添加了%d个字段'  %(tablename, count),
                create_time = time_now
                )
        # comment_list = MzxtCls.objects.all()
        else:
            res = FieldCls.objects.filter(tablename=fname).delete()
            RecordCls.objects.filter(tablename=fname).delete()
            LogCls.objects.create(
                app_name = u'媒资系统',
                add_content = fname,
                operator =  '删除了表【%s】'  %(fname),
                create_time = datetime.datetime.now()
                )

            print res
        mydict = {"errors":''}
        return HttpResponse(json.dumps(mydict),content_type="application/json")
