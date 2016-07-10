from django.conf.urls import url
from ZMXT.views import ZmxtView
from django.views.generic import TemplateView,DetailView

urlpatterns = [

        url(r'^zmxt/$',ZmxtView.as_view()),
]
