from django.db import models


# Марка машины
class Mark(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        db_table = 'mark'
        ordering = ['name']

    def __str__(self):
        return self.name


# Модель машины
class CarModel(models.Model):
    mark = models.ForeignKey(Mark, related_name='models', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'model'
        ordering = ['mark']

    def __str__(self):
        return self.name


# Задача (конкретный заказ на ремонт машины)
class Task(models.Model):
    mark = models.ForeignKey(Mark, related_name='related_tasks', default=0)
    model = models.ForeignKey(CarModel, related_name='tasks', on_delete=models.CASCADE)
    vin = models.CharField(max_length=17, unique=True)
    number = models.CharField(max_length=8, unique=True)
    date = models.DateTimeField()
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'task'
        ordering = ['-date']

    def __str__(self):
        return self.model.name + ' ' + str(self.date)


# Работы, предоставляемые мастерской
class Job(models.Model):
    name = models.CharField(max_length=30, unique=True)
    price = models.IntegerField()

    class Meta:
        db_table = 'job'
        ordering = ['name']

    def __str__(self):
        return self.name

    def serialize(self):
        return dict(id=self.id, job_name=self.name, price=self.price)


# Статус конкретной работы в конкретной задаче
class JobStatus(models.Model):
    task = models.ForeignKey(Task, related_name='status_tasks', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name='status_jobs', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'job_status'
        verbose_name_plural = 'Job statuses'

    def __str__(self):
        return str(self.task) + ' ' + str(self.job) + ' ' + str(self.status)
