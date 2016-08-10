#coding:utf-8
from MZXT.models import MzxtCls,FieldCls

import xadmin
from xadmin.layout import Main, Fieldset

class MzxtClsAdmin(object):
    list_filter = ('create_time',)
    fields = ('comment',)

class FieldClsAdmin(object):
    list_filter = ('create_time',)
    fields = ('tablename','field_name', 'field_type', 'ext')
    list_display = ('tablename','field_name','field_type','ext')
xadmin.site.register(MzxtCls,MzxtClsAdmin)
xadmin.site.register(FieldCls,FieldClsAdmin)

