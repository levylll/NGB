#coding:utf-8
from MZXT.models import MzxtCls

import xadmin
from xadmin.layout import Main, Fieldset

class MzxtClsAdmin(object):
    list_filter = ('create_time',)
    fields = ('comment',)


xadmin.site.register(MzxtCls,MzxtClsAdmin)

