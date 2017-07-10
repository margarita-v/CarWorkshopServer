from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.db import transaction
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
        # add info about job's statuses for each task
        jobs = [model_to_dict(job) for job in JobStatus.objects.filter(task=task['id'])]
        task['jobs'] = jobs
    return JsonResponse({'tasks': tasks})


# get all info about concrete task
def task_info(request, slug):
    slug = slug.lower()
    task = model_to_dict(get_object_or_404(Task, slug=slug))
    return JsonResponse(task)


# get all job statuses
def job_statuses_list(request):
    result = [model_to_dict(job_status) for job_status in JobStatus.objects.all()]
    return JsonResponse({'job_statuses': result})


# close job in task
@transaction.atomic
@require_POST
def close_job_in_task(request, task_id, job_id):
    task = get_object_or_404(Task, id=task_id)
    job = get_object_or_404(Job, id=job_id)
    job_status = get_object_or_404(JobStatus, task=task, job=job)
    job_status.status = True
    job_status.save()
    # check if all jobs in this task are closed
    found = False
    for job in JobStatus.objects.filter(task=task) and not found:
        found = job is False
    # we should close task if all of its jobs are closed
    if not found:
        task.status = True
        task.save()


# close concrete task
@transaction.atomic
@require_POST
def close_task(request):
    body_unicode = request.body.decode('utf-8')
    _data = json.loads(body_unicode)
    mark = _data['mark']
    print(mark)
    # return HttpResponse("OK")
    """task = get_object_or_404(Task, slug=slug)
    task.status = True
    task.save()
    for job_status in JobStatus.objects.filter(task=task):
        job_status.status = True
        job_status.save()"""


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


# close task or close chosen jobs in concrete task (using Django form)
@transaction.atomic
def edit_task(request, slug):
    slug = slug.lower()
    task = get_object_or_404(Task, slug=slug)
    data = {
        "mark": task.mark_id,
        "model": task.model_id,
        "vin": task.vin,
        "number": task.number,
        "slug": slugify(task.number),
        "date": str(task.date),
        "status": str(task.status)
    }
    url = 'http://localhost:8000/'
    client = requests.session()
    client.get(url)
    cookies = dict(client.cookies)
    headers = {'Content-type': 'application/json', "X-CSRFToken": client.cookies['csrftoken']}
    requests.post(url + "task/close/", headers=headers, data=json.dumps(data), cookies=cookies)
    return redirect('/')
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
