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


@transaction.atomic
def new_task(request):
    if request.method == "POST":
        form_task = AddTaskForm(request.POST)
        form_jobs = AddJobForm(request.POST)
        if form_task.is_valid() and form_jobs.is_valid():
            task = form_task.save(commit=False)
            task.slug = slugify(task.number)
            task.save()
            # get chosen job's names
            data = form_jobs.cleaned_data
            for job in data['jobs']:
                # find chosen job
                job = Job.objects.get(job_name=job)
                # create job status for current job in current task
                job_status = JobStatus()
                job_status.task = task
                job_status.job = job
                job_status.save()
            return redirect('/')
        else:
            return render(request, 'workshop/add_task.html', {'form_task': form_task, 'form_jobs': form_jobs})
    else:
        form_task = AddTaskForm()
        form_jobs = AddJobForm()
        return render(request, 'workshop/add_task.html', {'form_task': form_task, 'form_jobs': form_jobs})
