from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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
