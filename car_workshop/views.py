from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import AddTaskForm
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


def new_task(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.number)
            task.save()
            return redirect('/')
    else:
        form = AddTaskForm()
        return render(request, 'workshop/add_task.html', {'form': form})
