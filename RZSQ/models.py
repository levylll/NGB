#coding:utf-8
from django.db import models
from django.conf import settings

#用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,所以修改str类的title方法就可以实现.
class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

# Create your models here.
STATUS = {
        0: u'正常',
        1: u'草稿',
        2: u'删除',
}

#资讯来源
NEWS = {
        0: u'oschina',
        1: u'chiphell',
        2: u'freebuf',
        3: u'cnBeta',
}

class RzsqCls(models.Model):
    comment = models.TextField(verbose_name=u'消息内容')
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
    class Meta:
        verbose_name_plural = verbose_name = u'消息内容管理'
        ordering = ['-create_time']
        app_label = string_with_title('RZSQ',u"媒资系统管理")

    def __unicode__(self):
    # 在Python3中使用 def __str__(self)
        return self.comment