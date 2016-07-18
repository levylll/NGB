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
        table_names = list(set(FieldCls.objects.all().values_list('tablename', flat=True)))
        kwargs['table_list'] =  table_names

        return super(RZSQView,self).get_context_data(**kwargs)

    def get_queryset(self):
        comment_list = FieldCls.objects.all()
        return comment_list

    def post(self, request, *args, **kwargs):
        #获取评论
        valbuf = self.request.POST.get("comment","")
        #保存评论
        #comment = RzsqCls.objects.create(
                #comment = valbuf
                #)
        # comment_list = MzxtCls.objects.all()

        mydict = {"errors":""}
        return HttpResponse(json.dumps(mydict),content_type="application/json")
