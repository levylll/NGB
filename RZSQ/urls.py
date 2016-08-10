from django.conf.urls import url
from RZSQ.views import RZSQView
from django.views.generic import TemplateView,DetailView
from blog.models import News

urlpatterns = [

        url(r'^rzsq/$',RZSQView.as_view()),
        url(r'^rzsq/(?P<slug>\w+).html$',RZSQView.as_view()),
]
