from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^models/$', views.model_list, name='model_list'),
    url(r'^marks/$', views.mark_list, name='mark_list'),
    url(r'^jobs/$', views.job_list, name='job_list'),
    url(r'^tasks/$', views.task_list, name='task_list'),
    url(r'^(?P<mark_slug>[-\w]+)/$', views.model_list, name='model_list_by_mark'),
    url(r'^$', views.new_task, name='new_task'),
]
