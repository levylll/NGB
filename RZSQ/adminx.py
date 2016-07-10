#coding:utf-8
from RZSQ.models import RzsqCls

import xadmin
from xadmin.layout import Main, Fieldset

class RzsqClsAdmin(object):
    list_filter = ('create_time',)
    fields = ('comment',)


xadmin.site.register(RzsqCls,RzsqClsAdmin)

