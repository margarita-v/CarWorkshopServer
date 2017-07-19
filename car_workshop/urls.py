from django.conf.urls import url
from . import views


urlpatterns = [
    # GET requests
    url(r'^models/$', views.model_list, name='model_list'),  # get all car models
    url(r'^marks/$', views.mark_list, name='mark_list'),  # get all car marks
    url(r'^jobs/$', views.job_list, name='job_list'),  # get all jobs
    url(r'^job_statuses/$', views.job_statuses_list, name='job_statuses'),  # get all job statuses
    url(r'^tasks/$', views.task_list, name='task_list'),  # get all tasks
    url(r'^info/(?P<task_id>\d+)/$', views.task_info, name='task_info'),  # get info about task

    # POST requests
    url(r'^task/create/$', views.create_task, name='create_task'),  # create task
    url(r'^task/close/$', views.close_task, name='close_task'),  # close task
    url(r'^job/close/$', views.close_job_in_task, name='close_job'),  # close job
    url(r'^test/$', views.test, name='test'),  # test POST requests

    url(r'^(?P<mark_slug>[-\w]+)/$', views.model_list, name='model_list_by_mark'),  # get all models for concrete mark
    url(r'^$', views.new_task, name='new_task'),  # create a new task (using Django form)
]
