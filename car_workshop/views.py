from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import *
from .models import *

import requests
import json


# get all car marks
def mark_list(request):
    marks = [model_to_dict(mark) for mark in Mark.objects.all()]
    return JsonResponse({'marks': marks})


# get all models in database or get all models for concrete mark
def model_list(request, mark_slug=None):
    mark = None
    result = CarModel.objects.all()
    if mark_slug:
        # string lowercase
        mark_slug = mark_slug.lower()
        mark = get_object_or_404(Mark, slug=mark_slug)
        # get car models by mark id
        result = result.filter(mark=mark.id)
        # for JsonResponse
        mark = model_to_dict(mark)
    result = [model_to_dict(model) for model in result]
    return JsonResponse({'mark': mark, 'models': result})


# get all jobs
def job_list(request):
    jobs = [model_to_dict(job) for job in Job.objects.all()]
    return JsonResponse({'jobs': jobs})


# get all tasks
def task_list(request):
    tasks = [model_to_dict(task) for task in Task.objects.all()]
    for task in tasks:
        change_task_response(task)
    return JsonResponse({'tasks': tasks})


# get all info about concrete task
def task_info(request, task_id):
    task = model_to_dict(get_object_or_404(Task, id=task_id))
    return JsonResponse(change_task_response(task))


# get all job statuses
def job_statuses_list(request):
    result = [model_to_dict(job_status) for job_status in JobStatus.objects.all()]
    return JsonResponse({'job_statuses': result})


# create a new task
# send task fields and jobs as json array
@transaction.atomic
@require_POST
@csrf_exempt
def create_task(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    task = Task()
    task.mark_id = data['mark']
    task.model_id = data['model']
    task.date = data['date']
    task.vin = data['vin']
    task.number = data['number']
    task.number = task.number.upper()
    task.name = data['mark_name'] + ' ' + task.number + ' ' + str(task.date)
    task.save()
    for data_obj in data['jobs']:
        # deserialize job
        job = Job()
        job.id = data_obj['id']
        job.job_name = data_obj['job_name']
        job.price = data_obj['price']
        # create job status
        job_status = JobStatus()
        job_status.task = task
        job_status.job = job
        job_status.save()
    return HttpResponse("OK")


# close concrete task
# send task id
@transaction.atomic
@require_POST
@csrf_exempt
def close_task(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    task_id = data['id']
    task = get_object_or_404(Task, id=task_id)
    task.status = True
    task.save()
    for job_status in JobStatus.objects.filter(task=task_id):
        job_status.status = True
        job_status.save()
    return HttpResponse("OK")


# close concrete job in concrete task
# send task id and job_id
@transaction.atomic
@require_POST
@csrf_exempt
def close_job_in_task(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    task_id = data['task_id']
    job_id = data['job_id']
    job_status = get_object_or_404(JobStatus, task=task_id, job=job_id)
    job_status.status = True
    job_status.save()
    # check if all jobs in this task are closed
    found = False
    for job in JobStatus.objects.filter(task=task_id):
        found = job.status is False
        if found:
            break
    # we should close task if all of its jobs are closed
    if not found:
        task = get_object_or_404(Task, id=task_id)
        task.status = True
        task.save()
    return HttpResponse("OK")


# test POST requests
@transaction.atomic
def test(request):
    # for closing task
    # task/close
    data = {
        "task_id": 26
    }

    # for closing job in task
    # job/close
    data = {
        "task_id": 27,
        "job_id": 1
    }
    # for creation a new task
    # task/create
    """
    data = {
        "mark_name": "Ferrari",
        "mark": 7,
        "model": 21,
        "vin": "33345678909876543",
        "number": "o666ax",
        "date": "2012-04-05T20:40:45Z",
        "jobs": [
            {
                "id": 1,
                "price": 300,
                "job_name": "Замена масла в двигателе"
            },
            {
                "id": 2,
                "price": 600,
                "job_name": "Замена масляного фильтра"
            }
        ]
    }
    """
    url = 'http://localhost:8000/'
    headers = {'Content-type': 'application/json'}
    requests.post(url + "job/close/", headers=headers, data=json.dumps(data))
    return redirect('/')


# get info about jobs for each task
def change_task_response(task):
    task['jobs'] = [model_to_dict(job) for job in JobStatus.objects.filter(task=task['id'])]
    for job_status in task['jobs']:
        job_status['job'] = model_to_dict(Job.objects.get(id=job_status['job']))
    return task

"""
    # close task or close chosen jobs in concrete task (using Django form)
    slug = slug.lower()
    task = get_object_or_404(Task, slug=slug)
    # if task is open
    if request.method == "POST" and not task.status:
        # fill in task fields
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            # get chosen job's names
            data = form.cleaned_data['jobs']
            job_status_list = JobStatus.objects.filter(task=task)
            # if task is closed or if all jobs were chosen, then task will be closed
            if task.status or len(data) == len(job_status_list):
                # if all jobs were chosen, we should change task status
                task.status = True
                task.save()
                for job_status in job_status_list:
                    job_status.status = True
                    job_status.save()
            else:
                for job in data:
                    job = Job.objects.get(job_name=job)
                    job_status = JobStatus.objects.get(job=job, task=task)
                    job_status.status = True
                    job_status.save()
            return redirect('/')
    else:
        form = TaskForm(instance=task)
    return render(request, 'workshop/add_task.html', {'form': form})
    """


# create a new task (using Django form)
@transaction.atomic
def new_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.number)
            # we should create opened tasks only
            task.status = False
            task.save()
            # get chosen job's names
            data = form.cleaned_data['jobs']
            for job in data:
                # find chosen job
                job = Job.objects.get(job_name=job)
                # create job status for current job in current task
                job_status = JobStatus()
                job_status.task = task
                job_status.job = job
                job_status.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'workshop/add_task.html', {'form': form})
