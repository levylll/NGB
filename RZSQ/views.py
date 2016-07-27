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

class RZSQView(BaseMixin,ListView):
    template_name = 'blog/rzsq.html'
    context_object_name = 'comment_list'
    def get_context_data(self,**kwargs):
        #轮播
        table_list = list(set(FieldCls.objects.all().values_list('tablename', flat=True)))
        table_name = self.kwargs.get('slug','')
        col_list = FieldCls.objects.filter(tablename=table_name).values_list('field_name', flat=True)
        kwargs['table_list'] =  table_list
        kwargs['col_list'] =  col_list
        kwargs['cur_table'] =  table_name
        res = {}
        record_list = []
        record_raw = RecordCls.objects.filter(tablename=table_name).order_by('rowkey')
        for record in record_raw:
            if record.rowkey not in res:
                res[record.rowkey] = {}
            res[record.rowkey][record.field_name] = record.content
        for k,v in res.items():
            record_list.append(v)
        kwargs['record_list'] = record_list
        kwargs['records'] = res
        return super(RZSQView,self).get_context_data(**kwargs)

    def get_queryset(self):
        fieldset = FieldCls.objects.all()
        tablelist = []
        for elem in fieldset:
            if elem.tablename not in tablelist:
                tablelist.append(elem.tablename)
        return tablelist

    def insert_record(self, table, row_list):
        for elem in row_list:
            print '++++++'
            print elem
            time_now = datetime.datetime.now()
            seq = SeqCls.objects.create(create_time=time_now)
            cnt = 0
            for col, content in elem.items():
                RecordCls.objects.create(rowkey=seq.id, tablename=table, field_name=col, content=content, create_time=time_now)
                cnt += 1
        return cnt

    def clear_one(self, row_key):
        try:
            RecordCls.objects.filter(rowkey=row_key).delete()
        except Exception, err:
            print 'error %s' %str(err)
        return row_key

    def clear_all(self, table):
        try:
            RecordCls.objects.filter(tablename=table).delete()
        except Exception, err:
            print 'error %s' %str(err)
        return table

    def post(self, request, *args, **kwargs):
        #获取评论
        operate = self.request.POST.get("operate","")
        if operate == 'delete_one':
            rowkey = self.request.POST.get("rowkey","")
            self.clear_one(rowkey)
        elif operate == 'add':
            sendInfo = self.request.POST.get("sendInfo","")
            senddict = json.loads(sendInfo)
            self.insert_record(senddict['tablename'], senddict['rows'])
        elif operate == 'clear_table':
            table = self.request.POST.get("tablename","")
            self.clear_all(table)

        mydict = {"errors":""}
        return HttpResponse(json.dumps(mydict),content_type="application/json")
