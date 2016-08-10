#coding:utf-8
from DRMXT.models import LogCls

import xadmin
from xadmin.layout import Main, Fieldset

class DrmxtClsAdmin(object):
    list_filter = ('create_time',)
    fields = ('add_content',)

class LogClsAdmin(object):
    list_filter = ('create_time',)
    fields = ('add_content',)

xadmin.site.register(LogCls,LogClsAdmin)

