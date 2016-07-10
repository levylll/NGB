#coding:utf-8
from ZMXT.models import ZmxtCls

import xadmin
from xadmin.layout import Main, Fieldset

class ZmxtClsAdmin(object):
    list_filter = ('create_time',)
    fields = ('comment',)


xadmin.site.register(ZmxtCls,ZmxtClsAdmin)

