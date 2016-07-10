from django.conf.urls import url
from DSFYW.views import DSFYWView
from django.views.generic import TemplateView,DetailView
from blog.models import News

urlpatterns = [

        url(r'^dsfyw/$',DSFYWView.as_view()),
]
