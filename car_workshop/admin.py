from django.contrib import admin
from .models import *


class MarkAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('mark_name', )}


admin.site.register(Mark, MarkAdmin)
admin.site.register(CarModel)
admin.site.register(Task)
admin.site.register(Job)
admin.site.register(JobStatus)
