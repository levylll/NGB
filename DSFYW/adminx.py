#coding:utf-8
from DSFYW.models import DsfywCls

import xadmin
from xadmin.layout import Main, Fieldset

class DsfywClsAdmin(object):
    list_filter = ('create_time',)
    fields = ('comment',)


xadmin.site.register(DsfywCls,DsfywClsAdmin)

