from django.db import models


class QueueTask(models.Model):
    task_id = models.CharField(max_length=100, default=None)
    status = models.CharField(max_length=1, blank=True, null=True)
    name = models.CharField(max_length=50)

    list_display = ('name', 'status')
