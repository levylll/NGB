from django.conf.urls import url
from MZXT.views import MzxtView
from django.views.generic import TemplateView,DetailView

urlpatterns = [

        url(r'^mzxt/$',MzxtView.as_view()),
]
