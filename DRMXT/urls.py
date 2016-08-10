from django.conf.urls import url
from DRMXT.views import DRMXTView
from django.views.generic import TemplateView,DetailView
from blog.models import News

urlpatterns = [

        url(r'^drmxt/$',DRMXTView.as_view()),
]
