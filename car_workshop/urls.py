from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^jobs/$', views.job_list, name='job_list'),
    url(r'^models/$', views.model_list, name='model_list'),
    url(r'^(?P<mark_slug>[-\w]+)/$', views.model_list, name='model_list_by_mark'),
    url(r'^$', views.mark_list, name='mark_list'),
]
