from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.db import transaction

from .forms import *
from .models import *


def mark_list(request):
    marks = [model_to_dict(mark) for mark in Mark.objects.all()]
    return JsonResponse({'marks': marks})


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


def job_list(request):
    jobs = [model_to_dict(job) for job in Job.objects.all()]
    return JsonResponse({'jobs': jobs})


def task_list(request):
    tasks = [model_to_dict(task) for task in Task.objects.all()]
    for task in tasks:
        # add info about job's statuses for each task
        jobs = [model_to_dict(job) for job in JobStatus.objects.filter(task=task['id'])]
        task['jobs'] = jobs
    return JsonResponse({'tasks': tasks})


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


@transaction.atomic
def edit_task(request, slug):
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
