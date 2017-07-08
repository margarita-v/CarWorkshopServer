from django.contrib import admin
from .models import *


class MarkAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('mark_name', )}


class CarModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('model_name', )}


class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('number', )}


class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('job_name', )}


admin.site.register(Mark, MarkAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobStatus)
